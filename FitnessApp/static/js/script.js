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

document.addEventListener('DOMContentLoaded', function() {
    const postImages = document.querySelectorAll('.post img');
    postImages.forEach(function(img) {
        img.addEventListener('load', function() {
            
            const maxWidth = 200;
            const maxHeight = 200;
            if (img.width > maxWidth || img.height > maxHeight) {
                if (img.width / maxWidth > img.height / maxHeight) {
                    img.width = maxWidth;
                    img.height *= (maxWidth / img.width);
                } else {
                    img.height = maxHeight;
                    img.width *= (maxHeight / img.height);
                }
            }
        });
    });
});