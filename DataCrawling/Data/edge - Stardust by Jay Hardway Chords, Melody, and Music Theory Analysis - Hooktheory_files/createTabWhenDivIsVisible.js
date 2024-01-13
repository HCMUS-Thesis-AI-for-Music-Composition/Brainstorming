// @require theorytab-player

var pendingTheoryTabs = [];

function pushToPendingTheoryTabs(idOfDiv, params, inline = false) {
  var el = document.getElementById(idOfDiv);
  var rect = el.getBoundingClientRect();
  var top = rect.top;
  if (top >= 0 && top < window.innerHeight) {
    console.log(`pushToPendingTheoryTabs(${idOfDiv}) div already visible, creating`);
    if (inline) {
      theorytab.createInlineTab(idOfDiv, params);
    } else {
      theorytab.createTheoryTab(idOfDiv, params);
    }
  } else {
    // Push
    pendingTheoryTabs.push({
      idOfDiv: idOfDiv,
      params: params,
      inline,
    });
  }
}

function checkPendingTheoryTabs(e) {
  var el;
  for (var n = 0; n < pendingTheoryTabs.length; n++) {
    var el = document.getElementById(pendingTheoryTabs[n].idOfDiv);
    var rect = el.getBoundingClientRect();
    var top = rect.top;

    console.log(`checkPendingTheoryTabs() checking ${pendingTheoryTabs[n].idOfDiv} top: ${top}`);

    if (top >= 0 && top < window.innerHeight) {
      console.log(`checkPendingTheoryTabs() creating ${pendingTheoryTabs[n].idOfDiv}`);
      if (pendingTheoryTabs[n].inline) {
        theorytab.createInlineTab(pendingTheoryTabs[n].idOfDiv, pendingTheoryTabs[n].params);
      } else {
        theorytab.createTheoryTab(pendingTheoryTabs[n].idOfDiv, pendingTheoryTabs[n].params);
      }
      // Remove element from the list
      pendingTheoryTabs.splice(n, 1);
      n--;
    }
  }
}

window.addEventListener("scroll", checkPendingTheoryTabs);
