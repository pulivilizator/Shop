let slideIndex = 0;
showSlides();

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}
  slides[slideIndex-1].style.display = "block";
  setTimeout(showSlides, 7000); // Change image every 2 seconds
}

let sliderIndex = 1;
showSlidesM(sliderIndex);

// Next/previous controls
function plusSlidesM(n) {
  showSlidesM(sliderIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlidesM(sliderIndex = n);
}

function showSlidesM(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {sliderIndex = 1}
  if (n < 1) {sliderIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[sliderIndex-1].style.display = "block";
  dots[sliderIndex-1].className += " active";
}