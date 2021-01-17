var data = "";
var acceptSound = document.getElementById('accept-sound');
var rejectSound = document.getElementById('reject-sound');
var acceptPopup = document.getElementById('accept-popup');
var rejectPopup = document.getElementById('reject-popup');
var nametext = document.getElementById('name');
var statustext = document.getElementById('status');
var welcomeText = document.getElementById('welcome-text');


function accept() {
  acceptSound.currentTime = 0;
  acceptSound.play();
  acceptPopup.style.display = "block";
  setTimeout(function(){ acceptPopup.style.display = "none"; }, 1500);
}

function reject() {
  rejectSound.currentTime = 0;
  rejectSound.play();
  rejectPopup.style.display = "block";
  setTimeout(function(){ rejectPopup.style.display = "none"; }, 1500);
}

function decodeContinuously(codeReader, selectedDeviceId) {
  codeReader.decodeFromInputVideoDeviceContinuously(selectedDeviceId, 'video', (result, err) => {
    if (result) {
      // properly decoded qr code
      console.log('Found QR code!', result);

      if (result.text != data) {
        data = result.text;

        var surveyText = document.getElementById('survey_id');
        surveyText.parentElement.classList.add('is-dirty');
        surveyText.value = result.text;
        $.get( '/verify', $('#scanner-form').serialize()).done(response => 
        {
          if (response['check'] == true) {
            welcomeText.textContent = "Welcome " + response['name'] + "!";
            accept();
          }
          else {
            reject();
          }
          })
          .fail(function() {
            reject();
          });
        
      }
    }
  })
}

window.addEventListener('load', function () {
  let selectedDeviceId;
  const codeReader = new ZXing.BrowserQRCodeReader()
  console.log('ZXing code reader initialized')

  codeReader.getVideoInputDevices()
    .then((videoInputDevices) => {
      const sourceSelect = document.getElementById('sourceSelect')
      selectedDeviceId = videoInputDevices[0].deviceId
      if (videoInputDevices.length >= 1) {
        videoInputDevices.forEach((element) => {
          const sourceOption = document.createElement('option')
          sourceOption.text = element.label
          sourceOption.value = element.deviceId
          sourceSelect.appendChild(sourceOption)
        })

        sourceSelect.onchange = () => {
          selectedDeviceId = sourceSelect.value;
        };

        const sourceSelectPanel = document.getElementById('sourceSelectPanel')
        sourceSelectPanel.style.display = 'inline-block'
      }

      document.getElementById('startButton').addEventListener('click', () => {

        decodeContinuously(codeReader, selectedDeviceId);

        console.log(`Started decode from camera with id ${selectedDeviceId}`)
      })

      document.getElementById('resetButton').addEventListener('click', () => {
        codeReader.reset()
        var surveyText = document.getElementById('survey_id');
        surveyText.parentElement.classList.remove('is-dirty');
        surveyText.value = '';
        data = ""
        console.log('Reset.')
      })

    })
    .catch((err) => {
      console.error(err)
    })
});