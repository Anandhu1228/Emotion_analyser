var express = require('express');
var router = express.Router();
const { spawn } = require('child_process');

router.get('/', function(req, res, next) {
  res.render("user/testpage")
  return
});

router.post('/send_message', function(req, res, next) {
  let message_content = req.body.message.trim();
    const python = spawn('python', ['classifiers/classifier_file.py', message_content]);
  
    let result = '';
  
    python.stdout.on('data', function (data) {
      result += data.toString();
      console.log(`Python script output (stream): ${data.toString()}`);
    });
    
    python.stderr.on('data', function (data) {
      console.error(`stderr: ${data}`);
    });
    
    python.on('exit', function (code) {
      if (code === 0) {
        const resultTrimmed = result.trim().toLowerCase();
        res.send(resultTrimmed);
      } else {
        console.error('Error in Python script execution');
        res.status(500).send('Error processing the email content');
      }
    });  
});

module.exports = router;
