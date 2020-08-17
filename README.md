# teaching-jobs
Creates a notifier by email/text of new substitute job postings

Originally created this back in January/February of 2020 for my mother who is a substitute teacher.
In the surrounding Edmonton area, when a teacher at a school is planning on not being able to teach for a certain day a request for a substitute teacher is made to fill the vacancy. A listing then goes onto their password protected site where substitute teachers can take the job listing. The problem with this system is that substitute teachers (ie.my mom) have to regularly go onto each site and check if there are any job postings. This is very time consuming and having a simple notification system would save a lot of the substitute teachers free time.

This program uses the four websites (school boards) that my mother teaches at, signs her into each one on four different mozilla firefox web browsers and sends a notification via email/text message with the details of the job listing. The pages refreshes at a user defined rate and only new job listings are sent by notification with each listing having a clickable link for ease of signing in.

I originally tried to do this using requests thus removing the need to have the program open a browser but I was having difficulty getting past login pages and opted for the more simpler approach of automating the browser.

One major issue with this code was hard coding the password into the program. At this time I don't have much knowledge into password security and I tried to using PyInputPlus.inputPassword to convert the letters to asterisks upon entry but could not get it to work. 
