document.getElementById('profile').addEventListener('click', function(event){
  event.preventDefault();
  event.stopPropagation();
  const profileTab = document.getElementById('profile-tab');
  profileTab.style.display = (profileTab.style.display === 'block') ? 'none' : 'block';
});

document.addEventListener('click', function(event){
  const tab = document.getElementById('profile-tab');
  if(!tab.contains(event.target)){
    tab.style.display = 'none';
    console.log('xx');
  }
});
