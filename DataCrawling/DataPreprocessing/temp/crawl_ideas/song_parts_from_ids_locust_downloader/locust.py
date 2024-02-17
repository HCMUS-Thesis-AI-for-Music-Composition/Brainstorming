from locust import HttpUser, task

import random
import time
import utils as ut
import html_utils as hu

try:
    ut.fu.copy_folder_structure(
        ut.song_ids_of_song_parts_dir,
        ut.song_parts_from_ids_dir
    )
except Exception as e:
    print(e)

time_to_sleep_between_song_parts = random.uniform(2, 5)

letter_to_crawl = "a"
song_parts_list = ut.read_song_id_of_song_parts_list(letter_to_crawl)

class Downloader(HttpUser):
    host = "https://api.hooktheory.com/v1/songs/public/"
    song_parts_item = None

    def on_start(self):
        time_to_sleep = random.uniform(0, 1)
        time.sleep(time_to_sleep)
        global song_parts_list
        
        if len(song_parts_list) > 0:
            self.song_parts_item = song_parts_list.pop(0)
        else:
            self.song_parts_item = None

    def download(self):
        global time_to_sleep_between_song_parts

        song_part_ids = list(self.song_parts_item["song_parts_ids"])

        song_entire_data = dict(self.song_parts_item)

        song_entire_data["song_parts"] = []
        del song_entire_data["song_parts_ids"]

        for song_part_id in song_part_ids:
            song_part_url = f"{self.host}{song_part_id}"
            response = hu.make_request(self.client, song_part_url)

            if response["status_code"] == 200:
                song_entire_data["song_parts"].append(
                    {
                        "song_part_id": song_part_id,
                        "metadata": response["metadata"],
                        "main_data_type": response["main_data_type"],
                        "main_data": response["main_data"]
                    }
                )
            else:
                error_message = f"FAIL: download - status_code: {response['status_code']}, url: {song_part_url}"
                print(error_message)
                break

            time.sleep(time_to_sleep_between_song_parts)

        n_part_downloaded = len(song_entire_data["song_parts"])
        n_part_total = len(song_part_ids)
        song_link = self.song_parts_item["link"]

        if n_part_downloaded == n_part_total:
            json_relative_file_path = ut.fu.song_link_to_relative_html_file_path(song_link)
            json_relative_file_path = json_relative_file_path.replace(".html", ".json")

            ut.fu.write_data_to_json_file(
                song_entire_data,
                ut.fu.relative_to_absolute_path(
                    relative_path = json_relative_file_path,
                    root_path = ut.song_parts_from_ids_dir
                )
            )

            print(f"SUCCESS: {song_link}")
        else:
            print(f"ACK: {n_part_downloaded}/{n_part_total} part(s) downloaded - {song_link}")
            global song_parts_list
            song_parts_list.append(self.song_parts_item)
            print(f"--------> APPENDED BACK: {song_link}")

    @task
    def download_song_parts(self):
        if self.song_parts_item is not None:
            print(f"GETTING: {self.song_parts_item['link']}")
            self.download()
        else:
            print("INFO: download_song_parts - No more song to handle")
            self.environment.runner.quit()