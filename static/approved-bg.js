const possible = [
    'https://i.imgur.com/UEW1hwx.jpg',
    'https://i.imgur.com/fM3Av8a.jpg',
    'https://i.imgur.com/hUWO3ZY.jpg',
    'https://i.imgur.com/K8JyjXW.jpg',
    'https://i.imgur.com/mVBYiPv.jpg',
    'https://i.imgur.com/SRyM8UH.jpg',
    'https://i.imgur.com/iCJt8de.jpg',
    'https://i.imgur.com/03xDjcY.jpg',
    'https://i.imgur.com/id2wmS4.jpg',
    'https://i.imgur.com/ukyPAJC.jpg',
    'https://i.imgur.com/m0PcIDl.jpg',
    'https://i.imgur.com/Pbt42Bi.jpg',
    'https://i.imgur.com/YUpXCQp.jpg'
]
document.querySelector('.centered-parent').style.backgroundImage = `url('${possible[Math.floor(Math.random() * possible.length)]}')`