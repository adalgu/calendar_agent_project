/**
 * Google Calendar Integration Example
 * 
 * This file demonstrates how to programmatically interact with Google Calendar
 * using the Google Calendar API and MCP tools.
 */

// Required libraries for Google Calendar API
const fs = require('fs');
const readline = require('readline');
const {google} = require('googleapis');

// OAuth2 scopes for Google Calendar
const SCOPES = ['https://www.googleapis.com/auth/calendar'];
const TOKEN_PATH = 'token.json';

/**
 * Create an OAuth2 client with the given credentials
 * @param {Object} credentials The authorization client credentials
 */
function authorize(credentials) {
  const {client_secret, client_id, redirect_uris} = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(
      client_id, client_secret, redirect_uris[0]);

  // Check if we have previously stored a token
  try {
    const token = fs.readFileSync(TOKEN_PATH);
    oAuth2Client.setCredentials(JSON.parse(token));
    return oAuth2Client;
  } catch (err) {
    return getAccessToken(oAuth2Client);
  }
}

/**
 * Get and store new token after prompting for user authorization
 * @param {google.auth.OAuth2} oAuth2Client The OAuth2 client to get token for
 */
function getAccessToken(oAuth2Client) {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });
  console.log('Authorize this app by visiting this url:', authUrl);
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question('Enter the code from that page here: ', (code) => {
    rl.close();
    oAuth2Client.getToken(code, (err, token) => {
      if (err) return console.error('Error retrieving access token', err);
      oAuth2Client.setCredentials(token);
      // Store the token to disk for later program executions
      fs.writeFileSync(TOKEN_PATH, JSON.stringify(token));
      console.log('Token stored to', TOKEN_PATH);
      return oAuth2Client;
    });
  });
}

/**
 * Create work blocks in Google Calendar
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client
 * @param {Date} date Date to create blocks for
 * @param {Object} options Configuration options
 */
function createWorkBlocks(auth, date, options = {}) {
  const calendar = google.calendar({version: 'v3', auth});
  
  // Default options
  const config = {
    startHour: options.startHour || 10,
    endHour: options.endHour || 18,
    blockDuration: options.blockDuration || 45,
    breakDuration: options.breakDuration || 15,
    lunchStart: options.lunchStart || 12,
    lunchEnd: options.lunchEnd || 13,
    projectCode: options.projectCode || null
  };
  
  // Set up the date
  const startDate = new Date(date);
  startDate.setHours(config.startHour, 0, 0);
  
  const endDate = new Date(date);
  endDate.setHours(config.endHour, 0, 0);
  
  const lunchStartTime = new Date(date);
  lunchStartTime.setHours(config.lunchStart, 0, 0);
  
  const lunchEndTime = new Date(date);
  lunchEndTime.setHours(config.lunchEnd, 0, 0);
  
  // Create work blocks
  let currentTime = new Date(startDate);
  const createdEvents = [];
  
  while (currentTime < endDate) {
    // Skip lunch time
    if (currentTime >= lunchStartTime && currentTime < lunchEndTime) {
      currentTime = new Date(lunchEndTime);
      continue;
    }
    
    // Calculate block end time
    const blockEnd = new Date(currentTime);
    blockEnd.setMinutes(currentTime.getMinutes() + config.blockDuration);
    
    // Check if block would extend past end time
    if (blockEnd > endDate) {
      break;
    }
    
    // Create event title with project code if provided
    let summary = "Focus Work Block";
    if (config.projectCode) {
      summary = `[${config.projectCode}] ${summary}`;
    }
    
    // Create the event
    const event = {
      summary: summary,
      description: `${config.blockDuration}-minute focused work session`,
      start: {
        dateTime: currentTime.toISOString(),
        timeZone: 'UTC',
      },
      end: {
        dateTime: blockEnd.toISOString(),
        timeZone: 'UTC',
      },
      reminders: {
        useDefault: false,
        overrides: [
          {method: 'popup', minutes: 5},
        ],
      },
    };
    
    calendar.events.insert({
      auth: auth,
      calendarId: 'primary',
      resource: event,
    }, (err, res) => {
      if (err) {
        console.error('Error creating calendar event:', err);
        return;
      }
      console.log('Event created:', res.data.htmlLink);
      createdEvents.push(res.data);
    });
    
    // Move to next block (after break)
    currentTime = new Date(blockEnd);
    currentTime.setMinutes(currentTime.getMinutes() + config.breakDuration);
  }
  
  return createdEvents;
}

/**
 * Get events for a specific project code
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client
 * @param {string} projectCode Project code to filter by
 * @param {Date} startDate Start date for events
 * @param {Date} endDate End date for events
 */
function getProjectEvents(auth, projectCode, startDate, endDate) {
  const calendar = google.calendar({version: 'v3', auth});
  
  calendar.events.list({
    calendarId: 'primary',
    timeMin: startDate.toISOString(),
    timeMax: endDate.toISOString(),
    maxResults: 100,
    singleEvents: true,
    orderBy: 'startTime',
  }, (err, res) => {
    if (err) {
      console.error('Error fetching events:', err);
      return;
    }
    
    const events = res.data.items;
    
    // Filter events by project code
    const projectEvents = events.filter(event => {
      const summary = event.summary || '';
      return summary.includes(`[${projectCode}]`);
    });
    
    console.log(`Found ${projectEvents.length} events for project ${projectCode}`);
    
    projectEvents.forEach(event => {
      const start = event.start.dateTime || event.start.date;
      console.log(`${start} - ${event.summary}`);
    });
    
    return projectEvents;
  });
}

/**
 * Example usage of the calendar functions
 */
function main() {
  // Load client secrets from a local file
  fs.readFile('credentials.json', (err, content) => {
    if (err) {
      console.error('Error loading client secret file:', err);
      return;
    }
    
    // Authorize a client with credentials, then call the Google Calendar API
    const auth = authorize(JSON.parse(content));
    
    // Example: Create work blocks for tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    createWorkBlocks(auth, tomorrow, {
      projectCode: 'MAIN',
      startHour: 9,
      endHour: 17
    });
    
    // Example: Get events for a specific project in the next week
    const nextWeek = new Date();
    nextWeek.setDate(nextWeek.getDate() + 7);
    
    getProjectEvents(auth, 'SIDE', tomorrow, nextWeek);
  });
}

// Run the example if this file is executed directly
if (require.main === module) {
  main();
}

module.exports = {
  authorize,
  createWorkBlocks,
  getProjectEvents
};
