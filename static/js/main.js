const canvas = new fabric.Canvas('imageedit', {
    width: 512,
    height: 512
})

let img = data["image"];

var background = fabric.Image.fromURL(img, (imgdata) => {
    imgdata.set({
    scaleX: 1,
    scaleY: 1
    });
    canvas.setBackgroundImage(imgdata, canvas.renderAll.bind(canvas));
    canvas.renderAll();
});
