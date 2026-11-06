/**
 * Procedural Bottlecap Snapshot Renderer for BTLCAP Sidechain Showcase.
 * 100% self-contained client-side canvas rendering.
 */
(function() {
  const TIERS = {
    1: { name: 'Scrap', color: '#8b8b8b', border: '#5a5a5a', glowColor: null, pct: '60%' },
    2: { name: 'Brass', color: '#cd7f32', border: '#8b5a2b', glowColor: null, pct: '25%' },
    3: { name: 'Rad Silver', color: '#00e5ff', border: '#00b4d8', glowColor: 'rgba(0, 229, 255, 0.75)', pct: '10%' },
    4: { name: 'Vault Gold', color: '#ffd700', border: '#b8860b', glowColor: 'rgba(255, 215, 0, 0.85)', pct: '4%' },
    5: { name: 'Mythic Obsidian', color: '#e040fb', border: '#9c27b0', glowColor: 'rgba(224, 64, 251, 0.95)', pct: '1%' },
  };

  const METALS = {
    rust_iron: { outer: ['#4a4540', '#2d2926'], inner: ['#5c4a3d', '#3d2b1f'], rim: '#7a6252', highlight: '#8a7b70' },
    antiqued_brass: { outer: ['#b89038', '#5a4218'], inner: ['#c8a048', '#6a5220'], rim: '#d4af37', highlight: '#f3e5ab' },
    rad_silver: { outer: ['#a8b8c8', '#405060'], inner: ['#8098a8', '#384858'], rim: '#d8e8f8', highlight: '#ffffff' },
    gilded_gold: { outer: ['#ffd700', '#8b6914'], inner: ['#ffb700', '#996515'], rim: '#fff0a0', highlight: '#ffffff' },
    obsidian_carbon: { outer: ['#1a1a24', '#08080c'], inner: ['#222030', '#100e18'], rim: '#484060', highlight: '#8880a8' },
  };

  function renderCap(canvas, tierId, metalKey, symbolText) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const size = canvas.width;
    const center = size / 2;
    const radius = size * 0.40;

    ctx.clearRect(0, 0, size, size);

    const tier = TIERS[tierId] || TIERS[1];
    const metal = METALS[metalKey] || METALS.rust_iron;

    // 1. Glowing Corona (Tiers 3, 4, 5)
    if (tier.glowColor) {
      ctx.save();
      const glowGrad = ctx.createRadialGradient(center, center, radius * 0.7, center, center, radius * 1.25);
      glowGrad.addColorStop(0, tier.glowColor);
      glowGrad.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = glowGrad;
      ctx.beginPath();
      ctx.arc(center, center, radius * 1.25, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // 2. 21 Crimped Flutes
    const numFlutes = 21;
    const fluteRadius = radius * 1.12;
    ctx.save();
    for (let i = 0; i < numFlutes; i++) {
      const angle = (i * 2 * Math.PI) / numFlutes;
      const tipX = center + Math.cos(angle) * fluteRadius;
      const tipY = center + Math.sin(angle) * fluteRadius;

      ctx.beginPath();
      ctx.arc(tipX, tipY, size * 0.048, 0, Math.PI * 2);
      const fluteGrad = ctx.createRadialGradient(tipX - 2, tipY - 2, 1, tipX, tipY, size * 0.05);
      fluteGrad.addColorStop(0, metal.highlight);
      fluteGrad.addColorStop(0.5, metal.outer[0]);
      fluteGrad.addColorStop(1, '#0c0a08');
      ctx.fillStyle = fluteGrad;
      ctx.fill();
      ctx.strokeStyle = 'rgba(0,0,0,0.5)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
    ctx.restore();

    // 3. Outer Disc Body
    ctx.save();
    const outerGrad = ctx.createRadialGradient(center - radius * 0.3, center - radius * 0.3, radius * 0.1, center, center, radius);
    outerGrad.addColorStop(0, metal.outer[0]);
    outerGrad.addColorStop(0.85, metal.outer[1]);
    outerGrad.addColorStop(1, '#050403');
    ctx.fillStyle = outerGrad;
    ctx.beginPath();
    ctx.arc(center, center, radius, 0, Math.PI * 2);
    ctx.fill();

    // Metallic Rim Ring
    ctx.strokeStyle = metal.rim;
    ctx.lineWidth = size * 0.024;
    ctx.stroke();
    ctx.restore();

    // 4. Recessed Inner Cap Disc
    ctx.save();
    const innerRadius = radius * 0.82;
    const innerGrad = ctx.createRadialGradient(center - innerRadius * 0.2, center - innerRadius * 0.2, innerRadius * 0.1, center, center, innerRadius);
    innerGrad.addColorStop(0, metal.inner[0]);
    innerGrad.addColorStop(1, metal.inner[1]);
    ctx.fillStyle = innerGrad;
    ctx.beginPath();
    ctx.arc(center, center, innerRadius, 0, Math.PI * 2);
    ctx.fill();

    // Inner bevel shadow
    ctx.strokeStyle = 'rgba(0,0,0,0.6)';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.restore();

    // 5. Center Emblem
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = `bold ${size * 0.28}px "Share Tech Mono", monospace`;
    ctx.fillStyle = tier.color;
    ctx.shadowColor = tier.glowColor || 'rgba(0,0,0,0.8)';
    ctx.shadowBlur = tier.glowColor ? 12 : 4;
    ctx.fillText(symbolText, center, center);
    ctx.restore();

    // 6. Specular Curved Light Reflection
    ctx.save();
    ctx.beginPath();
    ctx.arc(center, center, innerRadius * 0.94, -Math.PI * 0.75, -Math.PI * 0.15);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.28)';
    ctx.lineWidth = size * 0.035;
    ctx.stroke();
    ctx.restore();
  }

  function initSnapshots() {
    const cards = [
      { id: 'cvs-tier-1', tier: 1, metal: 'rust_iron', sym: '⚙️' },
      { id: 'cvs-tier-2', tier: 2, metal: 'antiqued_brass', sym: '⚡' },
      { id: 'cvs-tier-3', tier: 3, metal: 'rad_silver', sym: '☢️' },
      { id: 'cvs-tier-4', tier: 4, metal: 'gilded_gold', sym: '👑' },
      { id: 'cvs-tier-5', tier: 5, metal: 'obsidian_carbon', sym: '💎' },
    ];

    cards.forEach((c) => {
      const el = document.getElementById(c.id);
      if (el) renderCap(el, c.tier, c.metal, c.sym);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSnapshots);
  } else {
    initSnapshots();
  }
})();

