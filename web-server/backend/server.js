const express = require('express');
const passport = require('passport');
const session = require('express-session');
const authRoutes = require('./routes/auth');
const dashboardRoutes = require('./routes/dashboard');
const uploadRoutes = require('./routes/upload');
const db = require('./db/sqlite.js');
const { init: initAuth } = require('./auth');
const path = require('path')
const cors = require("cors");
const imagesRoute = require("./routes/images");
const {wlogger, createMessage} = require('./winstonlogger.js');

const app = express();
const PORT = 8080;


app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));


app.use(cors());
app.use("/api/images", imagesRoute);
app.use("/api/upload", uploadRoutes);


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


db.sync({ force: false })
  .then(() => {
    app.listen(PORT, console.log('Server is running on port: ' + PORT));
  });

wlogger.info(createMessage( Date.now(), 'SUCCESS', 'Web-Server', 'server.js', '', '', 'Web-Server démarré avec succès'));
