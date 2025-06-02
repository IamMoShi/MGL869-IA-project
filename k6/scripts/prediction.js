import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

// import { readdirSync } from 'fs';
import { fs, open, SeekMode } from 'k6/experimental/fs';

const testDuration = __ENV.TEST_DURATION;
const sleep_duration = __ENV.TEST_SLEEP_DURATION;
const numberOfUsers = __ENV.NUMBER_OF_USERS;
const testType = parseInt(__ENV.TEST_TYPE, 10);

const rampUpPeriod = __ENV.RAMPS_UP_PERIOD;
const rampTarget = __ENV.RAMP_TARGET;

let options;

// // SMOKE test
if (testType === 1) {
  options = {
    vus: numberOfUsers,
    duration: testDuration,
  };
}

// SMOKE test type 2
if (testType === 2) {
  options = {
    stages: [
      { duration: '30s', target: 20 },
      { duration: '1m30s', target: 10 },
      { duration: '20s', target: 0 },
    ],
  };
}

// SPIKE Test
if (testType === 3) {
  options = {
      // Key configurations for spike in this section
      stages: [
        { duration: rampUpPeriod, target: rampTarget },   // fast ramp-up to a high point
        // No plateau
        { duration: '5s', target: 0 },      // quick ramp-down to 0 users
      ],
    };
}

// STRESS test  
if (testType === 4) {
  options = {
      // Key configurations for Stress in this section
      stages: [
        { duration: '10m', target: 200 }, // traffic ramp-up from 1 to a higher 200 users over 10 minutes.
        { duration: '30m', target: 200 }, // stay at higher 200 users for 30 minutes
        { duration: '5m', target: 0 }, // ramp-down to 0 users
      ],
    };
}

// BREAKPOINT test
if (testType === 5) {
  options = {
    // Key configurations for breakpoint in this section
    executor: 'ramping-arrival-rate', //Assure load increase if the system slows
    stages: [
      { duration: rampUpPeriod, target: rampTarget }, // just slowly ramp-up to a HUGE load
    ],
  };  
}

export { options };

// CLASSES = ["buildings", "forest", "glacier", "mountain", "sea", "street"]


// Function that will call the /userslist endpoint and check if the response contains the expected number of users
function predict(imgage, prediction_class) {
  const res = http.get('http://localhost:5000/api/v1/analyze/image/' + imgage);
  console.log(`Response code: ${res.status}`);

  check(res, {
    'is status 200': (r) => r.status === 200,
    'is response body not empty': (r) => r.body.length > 0,
  });

  const prediction = JSON.parse(res.body.prediction);
  console.log(res.body);
  
  sleep(randomIntBetween(0, sleep_duration));
}


export default function () {
  predict('11.jpg', 2); // Replace with the actual image file name you want to test
}

