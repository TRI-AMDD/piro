//import cucumber from 'cypress-cucumber-preprocessor';

//export default (on, config) => {
const cucumber = require('cypress-cucumber-preprocessor').default;
module.exports = (on, config) => {
  on('file:preprocessor', cucumber());

  on('task', {
    sendMail (message) {
      return sendAnEmail(message);
    }
  })
};


const sendAnEmail = (message) => {

    const nodemailer = require('nodemailer');
    const sgTransport = require('nodemailer-sendgrid-transport');
    const options = {
      auth: {
        api_user: 'sendgrid_USER',
        api_key: 'sendgrid_APIKEY'
      }
    }
    const client = nodemailer.createTransport(sgTransport(options));
  
    const email = {
      from: 'FROM_MAIL.PL',
      to: 'TO_MAIL.PL',
      subject: 'Hello',
      text: message,
      html: '<b>Hello world</b>'
    };
    client.sendMail(email, function(err, info) {
      return err? err.message : 'Message sent: ' + info.response;
    });
  }


