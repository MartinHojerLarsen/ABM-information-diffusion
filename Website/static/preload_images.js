// Image function

function prepare_image(id,path) {
    let elem = document.createElement('img');
    elem.src = path;
    elem.id = id;
    elem.style.display = 'none';
    document.body.append(elem);
}

// Commoner faces
prepare_image('commonerNormal','/static/img/commoner_normal.png');
prepare_image('commonerScared','/static/img/commoner_scared.png');
prepare_image('commonerHappy','/static/img/commoner_happy.png');

// F_influencer faces
prepare_image('finfluencerNormal','/static/img/finfluencer_normal.png');
prepare_image('finfluencerInfluencing','/static/img/finfluencer_influencing.png');
// R_influencer faces
prepare_image('rinfluencerNormal','/static/img/rinfluencer_normal.png');
prepare_image('rinfluencerInfluencing','/static/img/rinfluencer_influencing.png');