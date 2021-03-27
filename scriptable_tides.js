const width=130
const h=15
const w = new ListWidget()
w.backgroundColor=new Color("#222288")

/* update url below with the URL the python generated json file gets saved to */
const req = new Request("http://________.com/tides/todays_tides.json")
const res = await req.loadJSON();

getwidget2(10, 1, "🏖 Darien Tides")

Script.setWidget(w)
Script.complete()
w.presentSmall()

function getwidget2(total, haveGone, str) {
  const titlew = w.addText(str)
  titlew.textColor = new Color("#e5ffff")
  titlew.font = Font.boldMonospacedSystemFont(14)
  w.addSpacer(6)
  const imgw = w.addImage(creatProgress())
  imgw.imageSize=new Size(width, h)
  w.addSpacer(6)
  const st = w.addText("Next:" + res.nextTide + " " + res.nextTideTime)
  st.textColor = new Color("#e5ffff")
  st.font = Font.boldMonospacedSystemFont(11)
  w.addSpacer(6)
    
  var st1 = w.addText("Today's Tides:")
  st1.textColor = new Color("#cccccc")
  st1.font = Font.boldMonospacedSystemFont(11)
  w.addSpacer(4) 

  for (var i in res.todaysTides){
    var st2 = w.addText(res.todaysTides[i].tide + "   " + res.todaysTides[i].time + "   " + res.todaysTides[i].height + " ft")
    st2.textColor = new Color("#ffdd99")
    st2.font = Font.regularMonospacedSystemFont(8)
    w.addSpacer(3)   
  }
}

function creatProgress(){
    const context =new DrawContext()
    context.size=new Size(width, h)
    context.opaque=false
    context.respectScreenScale=true

    context.setFillColor(new Color("#ffdd99"))
    const path = new Path()
    path.addRoundedRect(new Rect(0, 0, width, h), 3, 2)
    context.addPath(path)
    context.fillPath()

    context.setFillColor(new Color("#0099ff"))
    const path1 = new Path()
    path1.addRoundedRect(new Rect(width/2, 0,res.tideLevel*width/200 , h), 0, 0)
    context.addPath(path1)
    context.fillPath()

    context.setFillColor(new Color("#222288"))
    const path2 = new Path()
    path2.addRoundedRect(new Rect((width/2)-4, 0, 4, h), 0, 0)
    context.addPath(path2)
    context.fillPath()

    context.setFillColor(new Color("#ff2222"))
    const path3 = new Path()
    path3.addRoundedRect(new Rect(((res.tideLevel+100)/2)*1.3, 0, 2, h), 0, 0)
    context.addPath(path3)
    context.fillPath()

    return context.getImage()
}