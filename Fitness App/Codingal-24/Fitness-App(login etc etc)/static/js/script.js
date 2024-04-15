function resizeImage(imageElement, maxWidth, maxHeight) {
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');
    let width = imageElement.width;
    let height = imageElement.height;

    if (width > height) {
        if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
        }
    } else {
        if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
        }
    }

    canvas.width = width;
    canvas.height = height;
    ctx.drawImage(imageElement, 0, 0, width, height);
    return canvas.toDataURL('image/jpeg', 0.7); 
}

document.addEventListener('DOMContentLoaded', function () {
    let images = document.querySelectorAll('.post img');
    images.forEach(function (image) {
        let newImage = new Image();
        newImage.src = image.src;
        newImage.onload = function () {
            let resizedImage = resizeImage(newImage, 200, 200);
            image.src = resizedImage;
        };
    });
});

