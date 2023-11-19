
const map=L.map('map').setView([-5.016389,-56.615833],9);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom:19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const customIcon=L.icon({iconUrl: 'icon-1.png', iconSize:[40,40]})


var data;
const uploadsuccess=document.getElementById("uploadsuccess").
    addEventListener("click", () => {
        Papa.parse(document.getElementById('UploadFile').files[0], {
            delimiter: ",",
            download: true,
            header: true,
            skipEmptyLines: true,
            complete: function (results) {
                console.log("hi");
                data = results.data;
                console.log(data);
                for(item of data){
                    var newCoord=convertCoordinates(item.coordinates);
                    console.log(newCoord);


                    var content=`<img src="images/1.jpg"><br><h1>${item.description}</h1><p>Date: ${item.date}<br> Time: ${item.time} <br>Location:  ${item.coordinates} </p>`
                    console.log(content);

                    
               
                    L.marker(newCoord,{icon: customIcon}).addTo(map)
                   .bindPopup(content,{offset:[0,-19]});
                }
            }
        });
    });

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




// L.marker([-5.016389,-56.615833],{icon: customIcon}).addTo(map)
//     .bindPopup('<img src="images/1.jpg"><br><h1>Fire in Forest</h1><p>Date: 2023/8/12<br> Time: 13:33 <br>Location: 5°41‘26\'\'S,57°3\'49\'\'W</p>',{offset:[0,-19]});
