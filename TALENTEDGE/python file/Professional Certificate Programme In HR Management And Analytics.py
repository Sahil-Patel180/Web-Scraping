import scrapy

class CourseSpider(scrapy.Spider):
    name = "courses"
    start_urls = [
        'https://talentedge.com/iim-kozhikode/professional-certificate-programme-in-hr-management-and-analytics'
    ]

    def parse(self, response):
        # Initial data extraction
        t1 = response.css('h1::text').get()
        t2 = response.css('h1 b::text').get()
        t3 = t1 + t2
        course_data = {
            'Course Link': response.url,
            'Title': t3,
            'Description': response.css('.desc_less p::text').get(),
            'Duration': response.css('.duration-of-course ul li p strong::text').get(),
            'Timing': response.css('.course-timing::text').get(),
            'Course Start Date': response.css('.duration-of-course ul li:nth-child(2) p strong::text').get(),
            'What you will Learn': response.css('.pl-deeper-undstnd.to_flex_ul ul li::text').getall(),
            'Skills': response.css('.key-skills-sec ul li::text').getall(),
            'Target Students': response.css('.cs-titlec::text').get(),
            'Prerequisites / Eligibility criteria': response.css('.eligible-right-top-list p::text').get(),
            'Content': response.css('.intabs li a::text').getall(),
            'Institute Name': response.css('.about-ititle::text').get(),
            'Fee in INR': response.css('.program-details-total-pay-amt-right::text').get(),
            'Fee in USD': response.css('.fee-in-usd::text').get(),
        }

        # Extracting faculty information and adding it directly to the course data
        faculty_sections = response.css('.best-fdetail')  # Adjust the selector to match the actual HTML structure

        for i, faculty in enumerate(faculty_sections, start=1):
            course_data[f'Faculty Name {i}'] = faculty.css('.best-fname::text').get()
            course_data[f'Faculty Designation {i}'] = faculty.css('.best-fdesingnation::text').get()
            course_data[f'Faculty Description {i}'] = faculty.css('.best-fknomore a::attr(data-description)').get()

        yield course_data
