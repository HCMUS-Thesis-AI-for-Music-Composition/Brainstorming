

// Use this for local
const host = "https://search.hooktheory.com"; //"http://127.0.0.1:7700";
const searchKey = "YHXUiQCa6024e2a88cb48f226a94d16db0c20d993e0a424cfde7834b697445bdf280ce88";

// Instantiate search client
const searchClient = instantMeiliSearch(host, searchKey, {
  placeholderSearch: false,
  primaryKey: "id", // default: undefined
  matches: true,
});

const indexName = "theorytabs";

// A port of Utils::prettyURLEncode for client-side
function prettyURLEncode(item) {
  item = item.toLowerCase();
  item = item.replace(/=/g, "-equals-");
  item = item.replace(/\+/g, "-plus-");
  item = item.replace(/\s+/g, "-");
  item = item.replace(/@/g, "-at-");
  item = item.replace(/&/g, "-and-");
  item = item.replace(/#/g, "-pound-");
  item = item.replace(/#/g, "-star-");
  item = item.replace(/%/g, "-percent-");
  item = item.replace(/\//g, "-slash-");
  item = item.replace(/[!,']/g, "");

  item = encodeURI(item);
  return item;
}

const getUrl = (item) => {
  return `/theorytab/view/${prettyURLEncode(item.artist)}/${prettyURLEncode(item.song)}`;
};

const indexOfMax = (arr) => {
  if (arr.length === 0) {
    return -1;
  }
  var max = arr[0];
  var maxIndex = 0;
  for (var i = 1; i < arr.length; i++) {
    if (arr[i] > max) {
      maxIndex = i;
      max = arr[i];
    }
  }
  return maxIndex;
};

var queryType = "name/artist";

const findLongestHighlight = (item) => {
  let attribute = "name/artist";
  const pat = /<mark>([^<]+)<\/mark>/;

  const artistMatch = item._highlightResult.artist.value.match(pat)?.[1]?.length || 0;
  const songMatch = item._highlightResult.song.value.match(pat)?.[1]?.length || 0;
  const chordAbsMatch = item._highlightResult.chordAbs.value.match(pat)?.[1]?.replace(/qq/g, "");
  const chordRelMatch = item._highlightResult.chordRel.value.match(pat)?.[1]?.replace(/qq/g, "");
  const chordSindMatch = item._highlightResult.SInD.value.match(pat)?.[1]?.replace(/qq/g, "");

  const chordAbsMatchCt = chordAbsMatch && !chordAbsMatch.match(/q/) ? chordAbsMatch.length : -1;
  const chordRelMatchCt = chordRelMatch && !chordRelMatch.match(/q/) ? chordRelMatch.length : -1;
  const chordSindMatchCt = chordSindMatch && !chordSindMatch.match(/q/) ? chordSindMatch.length : -1;

  const songArtistBuf = 1;
  const bestMatch = indexOfMax([
    artistMatch + songArtistBuf,
    songMatch + songArtistBuf,
    chordAbsMatchCt,
    chordRelMatchCt,
    chordSindMatchCt,
  ]);
  return ["name/artist", "name/artist", "chordAbs", "chordRel", "SInD"][bestMatch];
};

const arrowSnippet = (str) => {

  str = str.replace(/\s/g, ''); // trim spaces
  // Keep first mark only:
  let numMarks = str.match(/<mark>/g).length;
  while (numMarks >= 2) {
    str = str.replace(/\s*<mark>[^<]+<\/mark>[^<]*$/, "");
    numMarks = str.match(/<mark>/g).length;
  }

  // Truncate arrows at beginning or end of sequence:
  str = str.replace(/^<mark>qq/, "<mark>");
  str = str.replace(/qq<\/mark>$/, "</mark>");

  // Look ahead and grab one chord to the left of the highlight:
  const startMatch = str.match(/^<mark>[^<]+<\/mark>[^q]*qq/);
  str = startMatch ? startMatch[0] + "..." : str;

  const endMatch = str.match(/qq[^q]*<mark>[^<]+<\/mark>$/);
  str = endMatch ? "..." + endMatch[0] : str;

  const bothMatch = str.match(/qq[^q]*<mark>[^<]+<\/mark>[^q]*qq/);
  str = bothMatch ? "..." + bothMatch[0] + "..." : str;

  return str;
};

const queryHook = (query, search) => {
  if (query.match(/\s/)) {
    const absChordMatch = /^[a-gA-G][b#x]*[mdiaugøo+125679sud]*\/?[[a-gA-G]?[b#x]*$/;
    const relChordMatch = /^[b#x]*[viVI]+[øo+()b#12345679adsu]*\/?[b#x]*[viVI]*[øo+()b#12345679]*$/;
    const sindMatch = /^[JDYLMbCHT]*[12345679]+[b#12345679adsu]*\/?[12345679]*$/;

    const qSplt = query.split(" ");

    // greenlight a chord search if any of the above patterns match
    if (
      (qSplt[0].match(absChordMatch) && qSplt[1].match(absChordMatch)) ||
      (qSplt[0].match(relChordMatch) && qSplt[1].match(relChordMatch)) ||
      (qSplt[0].match(sindMatch) && qSplt[1].match(sindMatch))
    ) {
      query = query.replace(/\s+/g, "qq");
      query = query.replace(/&rarr;/g, "qq");
      query = query.replace(/[->]+/g, "qq");

      // swap slash:
      query = query.replace(/\//g, "slash");

      // if rel chord match, swap i and v for case sensitive:
      if (qSplt[0].match(relChordMatch) && qSplt[1].match(relChordMatch)) {
        query = query.replace(/i/g, "j");
        query = query.replace(/v/g, "w");
      }

      // Add leading and trailing delimiters
      if (!query.match(/^qq/)) {
        query = "qq" + query;
      }
      if (!query.match(/qq$/)) {
        query += "qq";
      }
    }
  }

  search(query);
};

const renderMeiliItemSongArtist = (item) => {
  return `<a href="${getUrl(item)}" class="a-no-decoration" title="${item.song} by ${item.artist}">
      <div class="overlay-trigger flex flex-align-items-center margin-bottom-10">
        <div class="width-50 margin-right-10">
          <div class="scalable-mask round div-content-overlay-centered-img" style="">
            <div class="">
              <img data-src="https://img.youtube.com/vi/${item.ytid}/mqdefault.jpg" class=" lazyloaded"
                src="https://img.youtube.com/vi/${item.ytid}/mqdefault.jpg">
            </div>
            <div class="div-overlay">
              <img src="/images/svg/product-icon-play-orange.svg">
            </div>
          </div>
        </div>
  
        <div class="flex flex-direction-column flex-justify-center line-height-1p2em color-text">
          <div>${instantsearch.highlight({ attribute: "song", hit: item })}</div>
          <div>by ${instantsearch.highlight({ attribute: "artist", hit: item })}</div>
        </div>
      </div>
    </a>`;
};

const renderItem = (item) => {
  // Check if this item is likely a chord, rel chord, or abs chord search:

  const longestHighlight = findLongestHighlight(item);

  switch (longestHighlight) {
    case "SInD":
    case "chordAbs":
    case "chordRel":
      let transform = (x) => {
        x = x.replace(/slash/g, "/");
        return x;
      };
      if (longestHighlight === "chordRel") {
        // swap i and v back:
        transform = (x) => {
          x = x.replace(/j/g, "i");
          x = x.replace(/w/g, "v");
          x = x.replace(/slash/g, "/");
          return x;
        };
      }

      return `<a href="${getUrl(item)}" class="a-no-decoration" title="${item.song} by ${item.artist}">
      <div class="overlay-trigger flex flex-align-items-center margin-bottom-10">
        <div class="width-50 margin-right-10">
          <div class="scalable-mask round div-content-overlay-centered-img" style="">
            <div class="">
              <img data-src="https://img.youtube.com/vi/${item.ytid}/mqdefault.jpg" class=" lazyloaded"
                src="https://img.youtube.com/vi/${item.ytid}/mqdefault.jpg">
            </div>
            <div class="div-overlay">
              <img src="/images/svg/product-icon-play-orange.svg">
            </div>
          </div>
        </div>
  
        <div class="flex flex-direction-column flex-justify-center line-height-1p2em color-text">
          <div>${item.song}</div>
          <div  class = "font-size-sm"> by ${item.artist}</div>
          <div class = "font-size-xs">${arrowSnippet(transform(item._highlightResult[longestHighlight].value)).replace(
            /qq/g,
            "&rarr;"
          )}</div>
        </div>
      </div>
    </a>`;

    case "name/artist":
    default:
      return renderMeiliItemSongArtist(item);
  }
};

// Create the custom widget
const placeholderElm = document.getElementById("theorytab-numsongs");
const placeholderText = placeholderElm ? placeholderElm.innerText.trim() : "Search 40k Songs";

// Instantiate desktop search
const search = instantsearch({
  indexName,
  searchClient,
});

// Set settings:
const configuration = {
  hitsPerPage: 10,
  attributesToSnippet: ["SInD:10", "chordAbs:10", "chordRel:10"],
};

search.addWidgets([
  instantsearch.widgets.configure(configuration),
  instantsearch.widgets.searchBox({
    placeholder: placeholderText,
    container: "#theorytab-searchbox",
    showSubmit: true,
    showReset: true,
    queryHook,
    // showReset: false,

    // see https://www.algolia.com/doc/api-reference/widgets/search-box/js/#widget-param-cssclasses
    cssClasses: {
      //root: ["hidden-xs", "hidden-sm"],
      //form: ["navbar-form", "navbar-left"],
      form: ["width-400"],
      input: [],
      submit: [],
      reset: [],
    },
    templates: {
      //loadingIndicator: '<i class="icon-spinner"></i>',
      submit: '<i class="icon-search"></i>',
      reset: '<i class="icon-cancel"></i>',
    },
  }),
  // instantsearch.widgets.stats({
  //   container: "#theorytab-stats",
  //   // Optional parameters
  //   //templates: object,
  //   //cssClasses: object,
  // }),
  instantsearch.widgets.infiniteHits({
    container: "#theorytab-hits",
    // Optional parameters
    //escapeHTML: boolean,
    templates: {
      item: renderItem,
      empty(results) {
        return ``;
      },
    },
    //cssClasses: object,
    //transformItems: function,
  }),
  // customHits({
  //   containerSearch: "#theorytab-searchbox",
  //   container: "#theorytab-hits",
  //   cssClasses: {
  //     root: ["border-radius-5", "width-100-percent", "padding-10", "shadow-sm", "background-white", "z-index-20", "position-absolute"],
  //   },
  // }),
]);

search.start();

// Instantiate mobile search
const searchMobile = instantsearch({
  indexName,
  searchClient,
});

searchMobile.addWidgets([
  instantsearch.widgets.configure(configuration),
  instantsearch.widgets.searchBox({
    placeholder: placeholderText,
    container: "#theorytab-searchbox-mobile",
    showSubmit: true,
    showReset: true,
    queryHook,

    // see https://www.algolia.com/doc/api-reference/widgets/search-box/js/#widget-param-cssclasses
    cssClasses: {
      //root: ["hidden-xs", "hidden-sm"], // on div that wraps form
      form: ["width-100-percent"],
    },
  }),
  instantsearch.widgets.infiniteHits({
    container: "#theorytab-hits-mobile",
    // Optional parameters
    //escapeHTML: boolean,
    templates: {
      item: renderItem,
      empty(results) {
        return ``;
      },
    },
    //cssClasses: object,
    //transformItems: function,
  }),
]);

searchMobile.start();
