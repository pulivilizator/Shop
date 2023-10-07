function showLikes() {
  let likeButton = document.getElementById('likes')
  likeButton.classList.add('active')
  let likesList = document.getElementById('likesList')
  likesList.classList.add('active')

  let orderButton = document.getElementById('orders')
  orderButton.classList.remove('active')
  let ordersList = document.getElementById('ordersList')
  ordersList.classList.remove('active')

  let settingsButton = document.getElementById('settings')
  settingsButton.classList.remove('active')
  let settingsList = document.getElementById('settingsList')
  settingsList.classList.remove('active')
}

function showOrders() {
  let likeButton = document.getElementById('likes')
  likeButton.classList.remove('active')
  let likesList = document.getElementById('likesList')
  likesList.classList.remove('active')

  let orderButton = document.getElementById('orders')
  orderButton.classList.add('active')
  let ordersList = document.getElementById('ordersList')
  ordersList.classList.add('active')

  let settingsButton = document.getElementById('settings')
  settingsButton.classList.remove('active')
  let settingsList = document.getElementById('settingsList')
  settingsList.classList.remove('active')
}

function showSettings() {
  let likeButton = document.getElementById('likes')
  likeButton.classList.remove('active')
  let likesList = document.getElementById('likesList')
  likesList.classList.remove('active')

  let orderButton = document.getElementById('orders')
  orderButton.classList.remove('active')
  let ordersList = document.getElementById('ordersList')
  ordersList.classList.remove('active')

  let settingsButton = document.getElementById('settings')
  settingsButton.classList.add('active')
  let settingsList = document.getElementById('settingsList')
  settingsList.classList.add('active')
}