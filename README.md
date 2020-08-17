# teaching-jobs
Creates a notifier by email/text of new substitute job postings

Originally created this back in January/February of 2020 for my mother who is a substitute teacher.
In the surround Edmonton area, when a teacher at a school is planning on not being able to teach for a certain day a request for a usbstitute teacher is made to fill the vacancy. A listing then goes onto their password protected site where substitutes can take the job listing.

This program uses the four websites (school boards) that my mother teaches at, signs her into each one on four different mozilla firefox web browsers and sends a notification via email/text message with the details of the job listing. The pages refreshes at a user defined rate and only new job listings are sent by notification with each listing having a clickable link for ease of signing in.

I originally tried to do this using requests thus removing the need to have the program open a browser but I was having difficulty getting past login pages and opted for the more simpler approach of automating the browser.
