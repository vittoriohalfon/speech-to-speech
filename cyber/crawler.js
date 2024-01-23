const axios = require('axios');
const cheerio = require('cheerio');
const cron = require('node-cron');
const puppeteer = require('puppeteer');
const robotParser = require('robots-parser');

const urls = ['https://example.com/page1', 'https://example.com/page2']; // Add your list of URLs here

const rateLimit = 2000; // Rate limit in milliseconds (2 seconds)

async function processUrlWithPuppeteer(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });

    const content = await page.content(); // serialized HTML of page
    // ... process the content as needed

    await browser.close();
}

// Function to process each URL
function processUrl(url) {
    axios.get(url)
        .then(response => {
            if (response.status === 200) {
                const html = response.data;
                const $ = cheerio.load(html);
                const text = $('body').text();
                console.log('URL:', url);
                console.log('Text:', text);

                $('img').each((i, elem) => {
                    console.log('Image src:', $(elem).attr('src'));
                });
            } else {
                console.error(`Error: Received a non-successful status code ${response.status}`);
            }
        })
        .catch(error => {
            if (error.response) {
                console.error(`Error: Server responded with status code ${error.response.status}`);
            } else if (error.request) {
                console.error('Error: No response received from the server');
            } else {
                console.error('Error:', error.message);
            }
        });
}

// Function to crawl URLs with rate limiting
function crawlUrls(urls, rateLimit) {
    let index = 0;
    const intervalId = setInterval(() => {
        if (index >= urls.length) {
            clearInterval(intervalId);
            return;
        }
        processUrl(urls[index]);
        index++;
    }, rateLimit);
}

// Schedule tasks to be run on the server.
cron.schedule('* * * * *', function() {
    console.log('Running a task every minute');
    crawlUrls(urls, rateLimit);
  });

// Start crawling
crawlUrls(urls, rateLimit);
