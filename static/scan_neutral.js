var survey_id = "";
var location_id = document.getElementById('loc_id').textContent;
var acceptSound = document.getElementById('accept-sound');
var rejectSound = document.getElementById('reject-sound');
var acceptPopup = document.getElementById('accept-popup');
var rejectPopup = document.getElementById('reject-popup');
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

      if (survey_id != result.text) {
        survey_id = result.text;
        
        $.get( '/verify', {survey_id: survey_id, loc_id: location_id}).done(response => 
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

    // if (err) {
    //   if (err instanceof ZXing.NotFoundException) {
    //     console.log('No QR code found.');
    //   }
    //   else if (err instanceof ZXing.ChecksumException) {
    //     console.log('A code was found, but it\'s read value was not valid.');
    //   }
    //   else if (err instanceof ZXing.FormatException) {
    //     console.log('A code was found, but it was in a invalid format.');
    //   }
    // }
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
