const express = require('express');
const passport = require('passport');
const session = require('express-session');
const authRoutes = require('./routes/auth');
const dashboardRoutes = require('./routes/dashboard');
const uploadRoutes = require('./routes/upload');
const predictRoutes = require('./routes/predict_image');
const db = require('./db.js');
const { init: initAuth } = require('./auth');
const path = require('path')
const env = require('dotenv').config();

const app = express();
const PORT = 8080;

app.use(express.urlencoded({extended: false}));
app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

initAuth();
app.use(session({
  secret: process.env.SESSION_SECRET,
  saveUninitialized: true,
  resave: true
}));

app.use(passport.initialize());
app.use(passport.session());

app.use('/', authRoutes);
app.use('/', dashboardRoutes);
app.use('/', uploadRoutes);
app.use('/', predictRoutes);

db.sync({ force: false })
  .then(() => {
    app.listen(PORT, console.log('Server is running on port: ' + PORT));
  });
