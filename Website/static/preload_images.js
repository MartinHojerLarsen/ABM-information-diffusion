// Image function

function prepare_image(id,path) {
    let elem = document.createElement('img');
    elem.src = path;
    elem.id = id;
    elem.style.display = 'none';
    document.body.append(elem);
}

prepare_image('commonerFace1','static/img/commoner_face1.png');
prepare_image('finfluencerFace1','static/img/finfluencer_face1.png');
prepare_image('rinfluencerFace1','static/img/rinfluencer_face1.png');