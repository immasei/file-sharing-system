//Credit https://site.uplabs.com/posts/windows-10-file-explorer
var isMoving = false;
var beginX = 0;
var beginY = 0;
var selectorX = 0;
var selectorY = 0;
var nowX = 0;
var nowY = 0;
var partenzaselettoreX;
var partenzaselettoreY;

function start(){
  	isMoving = true;
		beginX = window.event.clientX;
		beginY = window.event.clientY;
}

function trascina(){
  if(isMoving){
  	nowX = window.event.clientX;
		nowY = window.event.clientY;
					if(nowX > beginX){
						partenzaselettoreX = beginX;
					}else{
						partenzaselettoreX = nowX;
					}
    
          selectorX = Math.abs(beginX - nowX);
    
           if(nowY > beginY){
						  partenzaselettoreY = beginY;
					  }
					  else{
						  partenzaselettoreY = nowY;
					  }
    
    selectorY = Math.abs(beginY - nowY);
    
    $("#selettore").show();
    $("#selettore").css("margin-top",partenzaselettoreY);
    $("#selettore").css("margin-left",partenzaselettoreX);
    $("#selettore").css("width",selectorX);
    $("#selettore").css("height",selectorY);
  }
}

function stop(){
  isMoving = false;
  $("#selettore").hide();
}

const input = [
	{ 
	  type: 'folder', 
	  name: 'src', 
	  contents: [
		{
		  type: 'folder', 
		  name: 'doc', 
		  contents: [
			{ type: 'file', name: 'TOC.xlsx'},
			{ type: 'file', name: 'css.md'},
			{ type: 'file', name: 'extend.md'}
		  ]
		},
		{
		  type: 'folder',
		  name: 'img',
		  contents: [
			{ type: 'file', name: '.gitignore' },
			{ type: 'folder', 
			name: '.gitignore', 
			contents :[ 
			  { type: 'file', name: 'extend.md'},
			  { type: 'folder', name: 'extend.md', contents: [{ type: 'file', name: 'extend.md'}]}]}
		  ]
		},
		{
		  type: 'folder',
		  name: 'js',
		  contents: [
			{ type: 'file', name: 'main.js' },
			{ type: 'file', name: 'plugins.js' }
		  ]
		}
	  ]
	} 
  ];
  
const openKeys = ['src']

const renderFileTree = (el, data) => {
if(!el) return;
let treeHtml = '';

const dataLength = data.length;
for(let i = 0; i < dataLength; i++){
	treeHtml += getFileTreeHtml(data[i])
}

el.innerHTML = treeHtml;

const folderLinks = el.querySelectorAll('li.folder > a')
const folderLinksLength = folderLinks.length
for(let x = 0; x < folderLinksLength; x++)
{
	folderLinks[x].addEventListener('click', (e)=>{
	e.preventDefault();     
	const parentEl = e.currentTarget.parentNode;
	const iconEl = e.currentTarget.querySelector('i');
	if(parentEl.classList.contains('open')) {
		parentEl.classList.remove('open');
		iconEl.classList.remove('fa-folder-open');
		iconEl.classList.add('fa-folder');
	} else {
		parentEl.classList.add('open');
		iconEl.classList.remove('fa-folder');
		iconEl.classList.add('fa-folder-open');
	} 
	
	})
}
}
	
const getFileExtension = (filename) => {
if(!filename || filename.indexOf('.') === -1) return 'unknown'
const path = filename.toLowerCase().split('.')
return path[path.length-1]
}

const getFileTreeHtml = (data) => {
	let openClass = '';
	if(data.type === 'folder' && openKeys.indexOf(data.name) !== -1) openClass = 'open';
const ext = data.type === 'file' ? getFileExtension(data.name) : ''
	let html = `<li class="${data.type} ${openClass}"><a href="#"><i class="icon fa fa-${data.type}"></i> ${data.name}</a>`;
	// let html = `<li class="${data.type} ${openClass}"><a href="#"><i class="icon ${data.type} ext-${ext}"></i> ${data.name}</a>`;
	if(data.type === 'folder' && data.contents){
	html += '<ul class="folder-items">';
	const contentsLength = data.contents.length;
	for(let i = 0; i < contentsLength; i++){
		html += getFileTreeHtml(data.contents[i]);
	}
	html += '</ul>';
	}
	html += '</li>';
	
	return html;
}

renderFileTree(document.getElementById('tree'), input);