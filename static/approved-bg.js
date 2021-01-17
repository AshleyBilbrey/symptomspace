(function()
{
    const possible = [
        "/static/images/0.jpg",
        "/static/images/1.jpg",
        "/static/images/2.jpg",
        "/static/images/3.jpg",
        "/static/images/4.jpg",
        "/static/images/5.jpg",
        "/static/images/6.jpg",
        "/static/images/7.jpg",
        "/static/images/8.jpg",
        "/static/images/9.jpg",
        "/static/images/10.jpg",
        "/static/images/11.jpg"
    ]
    const bgContainer = document.querySelector('.centered-parent');
    bgContainer.style.backgroundImage = `url('${possible[Math.floor(Math.random() * possible.length)]}')`
    bgContainer.style.backgroundSize = 'cover';
    bgContainer.style.backgroundPosition = 'center';
    bgContainer.style.width = '100%';
    bgContainer.style.minHeight = '100%';
    bgContainer.style.height = 'min-content';
})()