const chart = document.querySelector('#chart');
const ctx = chart.getContext('2d');
const period = document.querySelector('#period');
const interval = document.querySelector('#interval');
const month = document.querySelector('#month');
const detail = document.querySelector('#detail');
const left = 38;
const right = 16;
function draw() {
  const rows = series.slice(+month.min, +month.max + 1);
  const selected = series[+month.value];
  const band = interval.checked && !interval.disabled;
  const values = rows.flatMap(r => band && r.low !== undefined ? [r.low, r.high] : [r.value]);
  const step = 20;
  const min = Math.floor(Math.min(0, ...values) / step) * step;
  const max = Math.max(step, Math.ceil(Math.max(...values) / step) * step);
  const w = chart.clientWidth, h = chart.clientHeight;
  const scale = window.devicePixelRatio || 1;
  chart.width = Math.round(w * scale);
  chart.height = Math.round(h * scale);
  ctx.scale(scale,scale);
  const x = i => left + i * (w-left-right) / (rows.length-1);
  const y = v => 12 + (max-v) * (h-42) / (max-min);
  ctx.font = '12px system-ui';
  ctx.textAlign = 'right';
  for(let v=min; v<=max; v+=step) {
    ctx.fillStyle='#526371'; ctx.fillText(v,left-6,y(v)+4);
    ctx.strokeStyle=v===0?'#80919b':'#dce1df'; ctx.beginPath();
    ctx.moveTo(left,y(v)); ctx.lineTo(w-right,y(v)); ctx.stroke();
  }
  ctx.textAlign='center';
  rows.forEach((r,i)=>{
    if(r.month.endsWith('-01')) ctx.fillText(r.month.slice(0,4),x(i),h-7);
  });
  const first = rows.findIndex(r=>r.low!==undefined);
  if(band && first>=0) {
    ctx.beginPath();
    for(let i=first;i<rows.length;i++) ctx.lineTo(x(i),y(rows[i].high));
    for(let i=rows.length-1;i>=first;i--) ctx.lineTo(x(i),y(rows[i].low));
    ctx.closePath();ctx.fillStyle='rgba(212,126,65,.23)';ctx.fill();
  }
  function line(start,end,color,dash) {
    if(end<=start) return;
    ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=2;ctx.setLineDash(dash);
    for(let i=start;i<end;i++) ctx.lineTo(x(i),y(rows[i].value));
    ctx.stroke();ctx.setLineDash([]);ctx.lineWidth=1;
  }
  line(0,first<0?rows.length:first,'#12636f',[]);
  if(first>=0) line(first,rows.length,'#a4421c',[6,4]);
  const cursor=x(+month.value-(+month.min));
  ctx.beginPath();ctx.strokeStyle='#526371';ctx.moveTo(cursor,12);ctx.lineTo(cursor,h-30);ctx.stroke();
  ctx.beginPath();ctx.fillStyle='#1d2e39';ctx.arc(cursor,y(selected.value),4,0,Math.PI*2);ctx.fill();
  const forecast=selected.low!==undefined;
  detail.textContent=selected.month+' · '+(forecast?'Forecast ':'Observed ')+selected.value.toFixed(forecast?2:1)+' sunspots'+(forecast && band?' · 95% interval '+selected.low.toFixed(2)+' to '+selected.high.toFixed(2):'');
  month.setAttribute('aria-valuetext',detail.textContent);
}
function setPeriod() {
  const firstForecast = series.findIndex(r=>r.low!==undefined);
  month.min = period.value==='forecast'?firstForecast:0;
  month.max = period.value==='history'?firstForecast-1:series.length-1;
  interval.disabled = period.value==='history';
  draw();
}
period.addEventListener('change',setPeriod);
interval.addEventListener('change',draw);
month.addEventListener('input',draw);
chart.addEventListener('pointermove', e=>{
  const fraction=(e.clientX-chart.getBoundingClientRect().left-left)/(chart.clientWidth-left-right);
  month.value=Math.round(+month.min+fraction*(month.max-month.min));
  draw();
});
new ResizeObserver(draw).observe(chart);
setPeriod();
