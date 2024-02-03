import os
import utils
import time

def scroll_to_bottom(browser, scroll_pause_time = 0.5):
    # Get the screen height of the web
    screen_height = browser.execute_script("return window.screen.height;") 
    i = 1

    max_scroll_times = 100

    while True:
        print(f"Scrolled: {i} time(s)")

        # Scroll one screen height each time
        browser.execute_script(
            f"window.scrollTo(0, {screen_height}*{i});"
        )
        
        time.sleep(scroll_pause_time)
        
        scroll_height = browser.execute_script(
            "return document.body.scrollHeight;"
        )

        i += 1
        if (screen_height) * i > scroll_height:
            break

        if i > max_scroll_times:
            print(f"Max scroll times reached")
            raise Exception("Max scroll times reached")
        
def scroll_and_get_html_content(url, browser):
    try:
        browser.get(url)
        scroll_to_bottom(browser)
        
        contents = browser.page_source

        return contents
    except:
        print(f"Failed to get {url}")
        raise Exception(f"Failed to get {url}")
    
def get_song_raw_html(url, browser):
    print(f"{url}: processing...")
    
    try:
        page_source = scroll_and_get_html_content(url, browser)

        path_to_save_html = utils.relative_to_absolute_path(
            utils.song_link_to_relative_html_file_path(url),
            root_path=utils.relative_to_absolute_path(
                "GetAllSongHTML/song_list/raw_html",
                root_path=utils.root_directory
            )
        )
        
        os.makedirs(os.path.dirname(path_to_save_html), exist_ok=True)

        utils.write_data_to_html_file(page_source, path_to_save_html)

        print(f"{url}: done")
    except:
        print(f"get_song_raw_html failed: {url}")
        raise Exception(f"get_song_raw_html failed")