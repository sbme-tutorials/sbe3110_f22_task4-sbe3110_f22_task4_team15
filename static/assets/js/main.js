import Cropper from 'cropperjs';

let magnitudeImageInput = document.querySelector("#magnitudeImageInput");
let phaseImageInput = document.querySelector("#phaseImageInput");
let magnitudeImage = document.querySelector(".magnitudeImage");
let magnitudeImageBtn = document.querySelector(".magnitudeImageBtn");
let phaseImageBtn = document.querySelector(".phaseImageBtn");
let phaseImage = document.querySelector(".phaseImage");
var path = "";

function upload_image_action(image,button) {
  image.style.display = `flex`;
  button.style.display = `none`;
}

magnitudeImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  magnitudeImage.style.display = `flex`;
  reader.addEventListener("load", () => {
    path = reader.result;
    magnitudeImage.src = `${path}`;
    upload_image_action(magnitudeImage,magnitudeImageBtn);
  });
  reader.readAsDataURL(this.files[0]);
});

phaseImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  phaseImage.style.display = `flex`;
  reader.addEventListener("load", () => {
    path = reader.result;
    phaseImage.src = `${path}`;
    upload_image_action(phaseImage,phaseImageBtn);
  });
  reader.readAsDataURL(this.files[0]);
});
function addImage(data) {
    let imageElement = new Image();
    imageElement.src = data;
    console.log(imageElement);
    let imageContainer = document.getElementById('reconstructedImageOutput');
    imageContainer.appendChild(imageElement);
}



const image = document.getElementById('image');
const cropper = new Cropper(image, {
  aspectRatio: 16 / 9,
  crop(event) {
    console.log(event.detail.x);
    console.log(event.detail.y);
    console.log(event.detail.width);
    console.log(event.detail.height);
    console.log(event.detail.rotate);
    console.log(event.detail.scaleX);
    console.log(event.detail.scaleY);
  },
});
addImage('');
