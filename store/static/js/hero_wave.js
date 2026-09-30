/**
 * SMASHPOINT — Real-Time 3D Interactive Wave Background
 * Powered by Three.js (WebGL)
 * Renders undulating aerodynamic waves symbolizing court speed & smash velocity
 */

(function () {
    let container, scene, camera, renderer;
    let particles, count = 0;
    let waveSpeed = 0.032;
    let waveHeight = 24;
    let mouseX = 0, mouseY = 0;
    let windowHalfX = window.innerWidth / 2;
    let windowHalfY = 260;

    const SEPARATION_X = 22;
    const SEPARATION_Y = 22;
    const AMOUNT_X = 90;
    const AMOUNT_Y = 60;
    const TOTAL_POINTS = AMOUNT_X * AMOUNT_Y;

    // Helper to generate soft luminous glow particle sprite
    function createGlowSprite() {
        const canvas = document.createElement('canvas');
        canvas.width = 32;
        canvas.height = 32;
        const ctx = canvas.getContext('2d');

        const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
        gradient.addColorStop(0.25, 'rgba(0, 242, 254, 0.9)');
        gradient.addColorStop(0.65, 'rgba(56, 189, 248, 0.35)');
        gradient.addColorStop(1, 'rgba(7, 11, 18, 0)');

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 32, 32);

        const texture = new THREE.Texture(canvas);
        texture.needsUpdate = true;
        return texture;
    }

    function init() {
        container = document.getElementById('heroWaveCanvasContainer');
        if (!container) return;

        // Scene setup
        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x070b12, 0.0011);

        const width = container.clientWidth || window.innerWidth;
        const height = container.clientHeight || 520;

        // Camera
        camera = new THREE.PerspectiveCamera(65, width / height, 1, 3000);
        camera.position.set(0, 210, 520);
        camera.lookAt(0, 20, 0);

        // Buffer Geometry for Particles
        const positions = new Float32Array(TOTAL_POINTS * 3);
        const colors = new Float32Array(TOTAL_POINTS * 3);

        let i = 0;
        for (let ix = 0; ix < AMOUNT_X; ix++) {
            for (let iy = 0; iy < AMOUNT_Y; iy++) {
                const posX = (ix * SEPARATION_X) - ((AMOUNT_X * SEPARATION_X) / 2);
                const posY = 0;
                const posZ = (iy * SEPARATION_Y) - ((AMOUNT_Y * SEPARATION_Y) / 2);

                positions[i] = posX;
                positions[i + 1] = posY;
                positions[i + 2] = posZ;

                // Color gradient (cyan to electric blue to indigo)
                const ratio = ix / AMOUNT_X;
                colors[i] = 0.0 + ratio * 0.2;     // R
                colors[i + 1] = 0.75 + ratio * 0.2; // G
                colors[i + 2] = 0.99;              // B

                i += 3;
            }
        }

        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 6,
            map: createGlowSprite(),
            vertexColors: true,
            blending: THREE.AdditiveBlending,
            transparent: true,
            opacity: 0.88,
            depthWrite: false
        });

        particles = new THREE.Points(geometry, material);
        scene.add(particles);

        // Ambient cyber grid mesh floor for depth
        const gridHelper = new THREE.GridHelper(2400, 48, 0x00f2fe, 0x1e293b);
        gridHelper.position.y = -65;
        gridHelper.material.opacity = 0.16;
        gridHelper.material.transparent = true;
        scene.add(gridHelper);

        // WebGL Renderer
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setSize(width, height);
        renderer.setClearColor(0x070b12, 0); // Transparent to blend seamlessly
        container.appendChild(renderer.domElement);

        // Listeners
        window.addEventListener('resize', onWindowResize, false);
        window.addEventListener('mousemove', onMouseMove, false);

        // Expose controls for live wave tuning
        window.setWavePreset = function (mode) {
            document.querySelectorAll('.wave-pill-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('waveBtn_' + mode);
            if (activeBtn) activeBtn.classList.add('active');

            if (mode === 'calm') {
                waveSpeed = 0.018;
                waveHeight = 14;
            } else if (mode === 'flow') {
                waveSpeed = 0.032;
                waveHeight = 24;
            } else if (mode === 'smash') {
                waveSpeed = 0.065;
                waveHeight = 40;
            }
        };

        animate();
    }

    function onMouseMove(event) {
        mouseX = (event.clientX - windowHalfX) * 0.35;
        mouseY = (event.clientY - windowHalfY) * 0.22;
    }

    function onWindowResize() {
        if (!container || !renderer || !camera) return;
        const width = container.clientWidth || window.innerWidth;
        const height = container.clientHeight || 520;
        windowHalfX = width / 2;
        windowHalfY = height / 2;

        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    }

    function animate() {
        requestAnimationFrame(animate);
        render();
    }

    function render() {
        // Camera smooth easing with mouse
        camera.position.x += (mouseX - camera.position.x) * 0.03;
        camera.position.y += (-mouseY + 200 - camera.position.y) * 0.03;
        camera.lookAt(0, 10, -30);

        const positionAttr = particles.geometry.attributes.position;
        const positions = positionAttr.array;
        const colorAttr = particles.geometry.attributes.color;
        const colors = colorAttr.array;

        let i = 0;
        for (let ix = 0; ix < AMOUNT_X; ix++) {
            for (let iy = 0; iy < AMOUNT_Y; iy++) {
                // Multi-frequency wave formula
                const wave1 = Math.sin((ix * 0.16) + count) * waveHeight;
                const wave2 = Math.cos((iy * 0.18) + (count * 0.75)) * (waveHeight * 0.75);
                const wave3 = Math.sin(((ix + iy) * 0.09) + (count * 1.2)) * (waveHeight * 0.45);

                const elevation = wave1 + wave2 + wave3;
                positions[i + 1] = elevation;

                // Color pulse based on wave crests
                const normHeight = (elevation + waveHeight) / (waveHeight * 2);
                colors[i] = 0.02 + normHeight * 0.28;        // Red (subtle magenta tint on peaks)
                colors[i + 1] = 0.60 + normHeight * 0.40;    // Cyan/Green
                colors[i + 2] = 0.98;                       // Blue glow

                i += 3;
            }
        }

        positionAttr.needsUpdate = true;
        colorAttr.needsUpdate = true;

        count += waveSpeed;
        renderer.render(scene, camera);
    }

    // Auto-init on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
