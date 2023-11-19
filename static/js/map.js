
var myData=
[
    {"coordinates_dms":"5º 41' 26\" S, 57º 3' 49\" W","description":"Operation ABC","file_url":"https://amazoniahack.s3.amazonaws.com/PHOTO-2023-10-13-14-52-20.jpg","filename":"PHOTO-2023-10-13-14-52-20.jpg","id":75,"picture_date":"2023-08-12","picture_time":"13:33:59","upload_date":"2023-11-19","upload_time":"14:21:46.305222"},
    {"coordinates_dms":"5º 16' 30\" S, 57º 32' 4\" W","description":"Operation XYZ","file_url":"https://amazoniahack.s3.amazonaws.com/PHOTO-2023-10-13-14-52-20_3.jpg","filename":"PHOTO-2023-10-13-14-52-20_3.jpg","id":76,"picture_date":"2023-08-13","picture_time":"11:15:30","upload_date":"2023-11-19","upload_time":"14:21:49.782815"},
    {"coordinates_dms":"5º 16' 30'' S, 57º 32' 5'' W","description":"Operation 1234","file_url":"https://amazoniahack.s3.amazonaws.com/PHOTO-2023-10-13-14-52-20_2.jpg","filename":"PHOTO-2023-10-13-14-52-20_2.jpg","id":77,"picture_date":"2023-08-13","picture_time":"11:07:06","upload_date":"2023-11-19","upload_time":"14:21:53.305918"}
  ];
const map=L.map('map').setView([-5.016389,-56.615833],9);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom:19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
const customIcon=L.icon({iconUrl: 'icon-1.png', iconSize:[40,40]})
for(item of myData){
    var newCoord=convertCoordinates(item.coordinates_dms);
    console.log(newCoord);
    var content=`<img src=${item.file_url}><br><h1>${item.description}</h1><p>Date: ${item.picture_date}<br> Time: ${item.picture_time} <br>Location:  ${item.coordinates_dms} </p>`
    console.log(content);
    L.marker(newCoord,{icon: customIcon}).addTo(map)
   .bindPopup(content,{offset:[0,-19]});
}
function convertCoordinates(coord){
    coord=coord.split(/[\'\"°,]/);
    var d1=parseFloat(coord[0]);
    var m1=parseFloat(coord[1]);
    var s1=parseFloat(coord[2]);
    var d2=parseFloat(coord[4]);
    var m2=parseFloat(coord[5]);
    var s2=parseFloat(coord[6]);
    var dd1 = -1*d1 + m1/60 + s1/3600;
    var dd2=-1*d2 + m2/60 + s2/3600
    return [dd1,dd2];
}