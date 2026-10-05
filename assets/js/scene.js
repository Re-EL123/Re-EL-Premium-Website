/* Re-EL Hero Scene — particles + stylised scarab/orbital system */
(function(){
  const canvas = document.getElementById('heroCanvas');
  if(!canvas) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.innerWidth < 768;

  let scene, camera, renderer, particles, scarabGroup, rings = [];
  let mouseX = 0, mouseY = 0, targetX = 0, targetY = 0;

  function init(){
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(55, canvas.clientWidth/canvas.clientHeight, 0.1, 1000);
    camera.position.z = 14;

    renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    resize();

    // particle field
    const count = isMobile ? 300 : 900;
    const positions = new Float32Array(count*3);
    for(let i=0;i<count;i++){
      positions[i*3] = (Math.random()-0.5)*40;
      positions[i*3+1] = (Math.random()-0.5)*24;
      positions[i*3+2] = (Math.random()-0.5)*20;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions,3));
    const mat = new THREE.PointsMaterial({ color:0xF6C945, size:0.06, transparent:true, opacity:0.6 });
    particles = new THREE.Points(geo, mat);
    scene.add(particles);

    // scarab-like core object (stylised, procedural — no external model required)
    scarabGroup = new THREE.Group();

    const bodyGeo = new THREE.IcosahedronGeometry(2.1, 1);
    const bodyMat = new THREE.MeshBasicMaterial({ color:0xF6C945, wireframe:true, transparent:true, opacity:0.55 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    scarabGroup.add(body);

    const coreGeo = new THREE.IcosahedronGeometry(1.1, 0);
    const coreMat = new THREE.MeshBasicMaterial({ color:0x21396A, wireframe:false, transparent:true, opacity:0.35 });
    scarabGroup.add(new THREE.Mesh(coreGeo, coreMat));

    // orbital rings
    const ringColors = [0xF6C945, 0x2F5EBB, 0xFFFFFF];
    for(let i=0;i<3;i++){
      const ringGeo = new THREE.TorusGeometry(3 + i*0.9, 0.01, 8, 100);
      const ringMat = new THREE.MeshBasicMaterial({ color: ringColors[i], transparent:true, opacity:0.35 });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = Math.PI/2 + i*0.4;
      ring.rotation.y = i*0.3;
      scarabGroup.add(ring);
      rings.push(ring);
    }

    scene.add(scarabGroup);

    window.addEventListener('resize', resize);
    if(!isMobile){
      window.addEventListener('mousemove', onMouseMove);
    }

    if(!prefersReduced) animate();
    else renderer.render(scene, camera);
  }

  function onMouseMove(e){
    targetX = (e.clientX / window.innerWidth - 0.5) * 2;
    targetY = (e.clientY / window.innerHeight - 0.5) * 2;
  }

  function resize(){
    const w = canvas.clientWidth || window.innerWidth;
    const h = canvas.clientHeight || window.innerHeight;
    camera.aspect = w/h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
  }

  function animate(){
    requestAnimationFrame(animate);
    mouseX += (targetX - mouseX) * 0.03;
    mouseY += (targetY - mouseY) * 0.03;

    scarabGroup.rotation.y += 0.0025 + mouseX*0.001;
    scarabGroup.rotation.x += 0.0008 + mouseY*0.0006;
    rings.forEach((r,i)=>{ r.rotation.z += 0.0015 * (i+1); });

    particles.rotation.y += 0.0006;

    camera.position.x += ( mouseX*1.2 - camera.position.x ) * 0.02;
    camera.position.y += ( -mouseY*1.2 - camera.position.y ) * 0.02;
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
  }

  if(window.WebGLRenderingContext){
    init();
  } else {
    canvas.style.display = 'none';
  }
})();
