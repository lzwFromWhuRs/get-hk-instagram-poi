from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

browser = webdriver.Chrome()

def main():
    sub_rgn_lnks=get_hk_sub_rgn_lnks()
    venue_names,venue_lnk=get_venue_names_from_sub_rgns(sub_rgn_lnks)


def get_hk_sub_rgn_lnks():
    """
    Get the sub regions under the page of https://www.instagram.com/explore/locations/hk/
    :return:
    """
    # HK_strt_lnk = "https://www.instagram.com/explore/locations/hk/"  # The start link of the city
    city_strt_lnk = "https://www.instagram.com/explore/locations/hk/"
    browser.get(city_strt_lnk)
    sub_rgn_lnks = []  # The list that stores the link of the subregion

    try:
        while 1:
            # Iteratively go to the next page until last page (throw NoSuchElementException)
            for i in range(0, len(browser.find_elements_by_class_name('aMwHK'))):
                sub_rgn_lnks.append(browser.find_elements_by_class_name('aMwHK')[i].get_attribute(
                    "href"))  # store the links of subregion in current page into sub_rgn_lnks
            nxt_pg_lnk = browser.find_element_by_class_name('PJ4k2').get_attribute("href")  # go to next page
            browser.get(nxt_pg_lnk)
    except NoSuchElementException:
        print("page link acquired")
    else:
        print("Unexpected Exception")
    finally:
        return sub_rgn_lnks
    # print(browser.page_source)


def get_venue_names_from_sub_rgns(sub_rgn_lnks):
    """
    Get the venue names under the sub regions
    :param sub_rgn_lnks:
    :return:
    """

    venue_names=[]
    venue_lnk=[]

    text_file = open("ins_hk_venues_names_url.txt",'w',encoding='utf-8')

    for i in range(0,len(sub_rgn_lnks)):
        browser.get(sub_rgn_lnks[i])
        try:
            while 1:
                # Iteratively go to the next page until last page (throw NoSuchElementException)
                for i in range(0, len(browser.find_elements_by_class_name('aMwHK'))):

                    venue_name=browser.find_elements_by_class_name('aMwHK')[i].text
                    v_lnk=browser.find_elements_by_class_name('aMwHK')[i].get_attribute("href")
                    venue_names.append(venue_name)  # store the links of subregion in current page into sub_rgn_lnks
                    venue_lnk.append(v_lnk)

                    text_file.write(str(venue_name) + ',' + str(v_lnk) + '\n') #write the poi name and url to txt

                nxt_pg_lnk = browser.find_element_by_class_name('PJ4k2').get_attribute("href")  # go to next page
                browser.get(nxt_pg_lnk)
        except NoSuchElementException:
            print("page link acquired")
        else:
            print("Unexpected Exception")
        finally:
            time.sleep(10)

    text_file.close()

    return venue_names, venue_lnk


main()