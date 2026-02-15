# Clamacalma — Guía de Estilo y Contexto

## Qué es
Landing page para un carpintero artesanal que fabrica juguetes de madera. Tienda boutique, fabricación a mano, contacto por WhatsApp.

## Marca
- **Nombre**: Clamacalma
- **Tono**: Cálido, artesanal, cercano. No corporativo. Hablamos de "juguetes hechos a mano" no de "productos".
- **Audiencia**: Padres/madres que buscan juguetes de calidad, naturales, no plástico.

## Paleta de colores
- `--cream: #FDF6EC` — fondo principal
- `--cream-dark: #F5EBD8` — fondo alternado
- `--wood: #C8956C` — acentos
- `--wood-dark: #A0724B` — títulos
- `--terracotta: #C67B5C` — botones secundarios
- `--sage: #8FA68A` — acentos sutiles
- `--text: #3D2E1F` — texto (marrón oscuro, NUNCA negro puro)
- `--text-light: #7A6B5D` — texto secundario
- `--dark: #1a1a2e` — sección 3D solamente
- `--whatsapp: #25D366` — botón WhatsApp

## Tipografía
- **Títulos**: `'Playfair Display', Georgia, serif`
- **Cuerpo**: `'Inter', 'Segoe UI', sans-serif`
- **Marca**: Playfair Display, letter-spacing 0.15em

## Principios de diseño
1. **Cálido, no tech** — Las fotos y la madera son protagonistas, no la tecnología
2. **Artesanal** — Bordes suaves, texturas sutiles, nada angular ni "flat"
3. **Boutique** — Espaciado generoso, pocas palabras, que respire
4. **Infantil sin ser infantiloide** — Colores tierra, no primarios brillantes
5. **Mobile-first** — Todo debe verse impecable en celular

## Stack técnico
- HTML + CSS + JS vanilla (sin frameworks)
- CSS custom properties + Grid + Flexbox
- Google Fonts (Playfair Display + Inter)
- Three.js solo dentro de los iframes de modelos 3D
- Fotos en `downloads/clamacalma/[Categoría]/`

## Modelos 3D existentes
- `tangram3d/` — Tangram 7 piezas
- `arcoiris3d/` — Arco iris Waldorf
- `jenga3d/` — Torre Jenga
- `cubosoma3d/` — Cubo Soma
- `tateti3d/` — Ta-Te-Ti
- Cada uno es un HTML autocontenido con fondo `#1a1a2e`, OrbitControls, drag

## WhatsApp
- Número: PLACEHOLDER (pendiente)
- Formato: `https://wa.me/PLACEHOLDER?text=...`
- Mensaje default: "Hola! Me interesan los juguetes de Clamacalma"
- Mensaje por producto: "Hola! Me interesa el [nombre] de Clamacalma"
