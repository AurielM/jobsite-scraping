from playwright.sync_api import sync_playwright


class JobScraper:

    def __init__(self, playwright):
        self.chromium = playwright.chromium
        self.browser = self.chromium.launch(headless=False)
        self.page = self.browser.new_page()

        # page objects
        self.google_box = self.page.locator("button.icl-CloseButton")
        self.cookie_accept = self.page.locator("button#onetrust-accept-btn-handler")
        self.sign_up_bait = self.page.get_by_role("button", name="close")

        self.wrapper_dropdown_remote = self.page.locator("div.yosegi-FilterPill-dropdownPillContainer").nth(2)
        self.dropdown_remote = self.wrapper_dropdown_remote.locator("ul[role=menu]").locator("li[role=menuitem]").nth(0)

        self.field_search = self.page.get_by_placeholder("Job title, keywords, or company")
        self.button_search = self.page.get_by_role("button", name="Find jobs")
        self.button_job_title = self.page.locator("a.jcs-JobTitle")
        self.text_job_description = self.page.locator("div#jobDescriptionText")


        # search criteria
        self.title_must_haves = ["Junior"]
        # self.title_should_have_one = ["developer", "software", "automation", "tester", "test", "engineer"]
        self.body_must_haves = ["python"]
        self.must_not_haves = ["intern"]

    def run(self):

        self.page.goto("https://uk.indeed.com/?r=us")
        self.remove_covering_boxes()
        self.field_search.fill('junior software developer')
        self.button_search.click()

        self.page.wait_for_load_state(state="networkidle")
        self.wrapper_dropdown_remote.click()
        self.dropdown_remote.click()

        self.remove_covering_boxes()

        self.job_title_scraping()
        print('Scraping complete')
        self.browser.close()

    def remove_covering_boxes(self):
        self.page.wait_for_load_state(state="networkidle")
        if self.google_box.is_visible():
            self.google_box.click()
        if self.cookie_accept.is_visible():
            self.cookie_accept.click()
        if self.sign_up_bait.is_visible():
            self.sign_up_bait.click()

    def job_title_scraping(self):
        self.button_job_title.nth(0).wait_for(state="visible")
        # ^page registers as loaded when all the links aren't present^

        for job_title in self.button_job_title.all():
            self.page.pause()
            job_title.click()
            self.remove_covering_boxes()
            for must_have in self.title_must_haves:
                print(f'must have: {must_have}')
                if must_have in job_title.inner_text(): # code breaking here
                    print(f'must have: {must_have} is in job_title: {job_title.inner_text()}')
                    job_title.click()
                    self.remove_covering_boxes()
                    for must_have1 in self.body_must_haves:
                        print(f'must have1: {must_have1}')
                        if must_have1 in self.text_job_description.inner_text():
                            print(f'must have1: {must_have} is in job_title: {self.text_job_description}')
                            print(f'job title: {job_title.inner_text()}\nURL: {self.button_job_title.url()}')
                    self.page.pause()
                    break


with sync_playwright() as playwright:
    JobScraper(playwright).run()
