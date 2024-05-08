function showProperties() {
  let prop_button = document.getElementsByClassName('properties')
  prop_button[0].classList.add('active')

  specifics = document.getElementsByClassName('product__properties')
  specifics[0].style.display = 'flex'

  let rev_button = document.getElementsByClassName('reviews')
  rev_button[0].classList.remove('active')

  let reviews = document.getElementsByClassName('product__reviews')
  reviews[0].style.display = 'none'
}

function showReviews() {
  let prop_button = document.getElementsByClassName('properties')
  prop_button[0].classList.remove('active')

  specifics = document.getElementsByClassName('product__properties')
  specifics[0].style.display = 'none'

  let rev_button = document.getElementsByClassName('reviews')
  rev_button[0].classList.add('active')

  let reviews = document.getElementsByClassName('product__reviews')
  reviews[0].style.display = 'flex'
}