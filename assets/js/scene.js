/* Re-EL Hero Scene — particles + stylised emblem/orbital system */
(function(){
  const canvas = document.getElementById('heroCanvas');
  if(!canvas || typeof window.THREE === 'undefined'){
    if(canvas) canvas.style.display = 'none';
    return;
  }

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.innerWidth < 768;

  let scene, camera, renderer, particles, emblem, rings = [];
  let frame = 0;
  let mouseX = 0, mouseY = 0, targetX = 0, targetY = 0;

  function buildScene(){
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(55, 1, 0.1, 1000);
    camera.position.z = 14;

    // Context creation can throw even when the WebGL API exists
    // (blocked driver, headless, exhausted contexts).
    try{
      renderer = new THREE.WebGLRenderer({
        canvas,
        antialias:true,
        alpha:true,
        powerPreference:'high-performance'
      });
    }catch(err){
      canvas.style.display = 'none';
      return false;
    }

    renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2));
    resize();

    // particle field
    const count = isMobile ? 240 : 900;
    const positions = new Float32Array(count * 3);
    for(let i = 0; i < count; i++){
      positions[i*3]     = (Math.random() - 0.5) * 40;
      positions[i*3 + 1] = (Math.random() - 0.5) * 24;
      positions[i*3 + 2] = (Math.random() - 0.5) * 20;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particles = new THREE.Points(geo, new THREE.PointsMaterial({
      color:0xD6AE01, size:0.06, transparent:true, opacity:0.6
    }));
    scene.add(particles);

    // emblem core (procedural — no external model required)
    emblem = new THREE.Group();

    const bodyMat = new THREE.MeshBasicMaterial({
      color:0xD6AE01, wireframe:true, transparent:true, opacity:0.55
    });
    emblem.add(new THREE.Mesh(new THREE.IcosahedronGeometry(2.1, 1), bodyMat));

    const coreMat = new THREE.MeshBasicMaterial({
      color:0x1E3A6E, wireframe:false, transparent:true, opacity:0.45
    });
    emblem.add(new THREE.Mesh(new THREE.IcosahedronGeometry(1.1, 0), coreMat));

    // orbital rings
    const ringColors = [0xD6AE01, 0x2F5EBB, 0xFFFFFF];
    for(let i = 0; i < 3; i++){
      const ringMat = new THREE.MeshBasicMaterial({
        color:ringColors[i], transparent:true, opacity:0.3
      });
      const ring = new THREE.Mesh(new THREE.TorusGeometry(3 + i*0.9, 0.01, 8, 100), ringMat);
      ring.rotation.x = Math.PI/2 + i*0.4;
      ring.rotation.y = i*0.3;
      rings.push(ring);
      emblem.add(ring);
    }

    scene.add(emblem);
    return true;
  }

  function onMouseMove(e){
    targetX = (e.clientX / window.innerWidth  - 0.5) * 2;
    targetY = (e.clientY / window.innerHeight - 0.5) * 2;
  }

  function resize(){
    const w = canvas.clientWidth  || window.innerWidth;
    const h = canvas.clientHeight || window.innerHeight;
    if(!w || !h) return;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
  }

  function animate(){
    frame = requestAnimationFrame(animate);

    mouseX += (targetX - mouseX) * 0.03;
    mouseY += (targetY - mouseY) * 0.03;

    emblem.rotation.y += 0.0025 + mouseX * 0.001;
    emblem.rotation.x += 0.0008 + mouseY * 0.0006;
    rings.forEach((ring, i) => { ring.rotation.z += 0.0015 * (i + 1); });

    particles.rotation.y += 0.0006;

    camera.position.x += ( mouseX * 1.2        - camera.position.x) * 0.02;
    camera.position.y += (-mouseY * 1.2        - camera.position.y) * 0.02;
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
  }

  function play(){ if(!frame) animate(); }
  function pause(){ if(frame){ cancelAnimationFrame(frame); frame = 0; } }

  if(buildScene()){
    window.addEventListener('resize', resize);
    if(!isMobile) window.addEventListener('mousemove', onMouseMove, { passive:true });

    if(reduced){
      renderer.render(scene, camera);
    } else {
      play();

      // Don't burn CPU/GPU once the hero has scrolled away.
      const hero = document.querySelector('.hero');
      if(hero && 'IntersectionObserver' in window){
        new IntersectionObserver(([entry]) => {
          entry.isIntersecting && !document.hidden ? play() : pause();
        }, { threshold:0 }).observe(hero);
      }

      document.addEventListener('visibilitychange', () => {
        document.hidden ? pause() : play();
      });
    }
  }
})();
