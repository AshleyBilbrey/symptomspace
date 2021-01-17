var data = "";
var accept = document.getElementById('accept');
var reject = document.getElementById('reject');
var nametext = document.getElementById('name');
var statustext = document.getElementById('status');

function decodeContinuously(codeReader, selectedDeviceId) {
  codeReader.decodeFromInputVideoDeviceContinuously(selectedDeviceId, 'video', (result, err) => {
    if (result) {
      // properly decoded qr code
      console.log('Found QR code!', result);

      if (result.text != data) {
        var surveyText = document.getElementById('survey_id');
        surveyText.parentElement.classList.add('is-dirty');
        surveyText.value = result.text;
        data = result.text;
      }
    }

    if (err) {
      if (err instanceof ZXing.NotFoundException) {
        console.log('No QR code found.');
      }
      else if (err instanceof ZXing.ChecksumException) {
        console.log('A code was found, but it\'s read value was not valid.');
      }
      else if (err instanceof ZXing.FormatException) {
        console.log('A code was found, but it was in a invalid format.');
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
