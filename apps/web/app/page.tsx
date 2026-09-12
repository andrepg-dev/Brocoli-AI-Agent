import Image from 'next/image'
import styles from './page.module.css'

const navItems = [
  { href: '#producto', label: 'Comer mejor' },
  { href: '#como-funciona', label: 'Brócoli' },
  { href: '#preguntas', label: 'Preguntas' },
]

const localStores = [
  {
    name: 'Paiz',
    logo: '/store-paiz.svg',
    width: 117,
    height: 40,
  },
  {
    name: 'Walmart Honduras',
    logo: '/store-walmart.png',
    width: 143,
    height: 34,
    dark: true,
  },
  {
    name: 'La Colonia',
    logo: '/store-la-colonia.png',
    width: 106,
    height: 60,
  },
  {
    name: 'Maxi Despensa',
    logo: '/store-maxi-despensa.png',
    width: 132,
    height: 48,
  },
]

const benefits = [
  {
    number: '01',
    title: 'Aumenta tu energía',
    copy: 'Desayunos y comidas completas para sentirte con energía durante todo el día.',
    image: '/benefit-energy-pexels.jpg',
    alt: 'Dos mujeres corriendo juntas en una pista al aire libre',
  },
  {
    number: '02',
    title: 'Come variado toda la semana',
    copy: 'Desayunos, almuerzos y cenas saludables sin repetir siempre lo mismo.',
    image: '/benefit-plan-pexels.jpg',
    alt: 'Comida saludable preparada con pollo, brócoli y vegetales',
  },
  {
    number: '03',
    title: 'Compra solo lo necesario',
    copy: 'Aprovecha primero lo que tienes en casa y compra únicamente lo que hace falta.',
    image: '/benefit-shopping-pexels.jpg',
    alt: 'Persona comprando vegetales frescos en un supermercado',
  },
]

const faqs = [
  {
    question: '¿Brócoli reemplaza a un nutricionista?',
    answer:
      'No. Brócoli está pensado para ayudarte a comer mejor cada día. Para condiciones médicas o necesidades clínicas, consulta a un profesional de salud.',
  },
  {
    question: '¿Necesito comprar ingredientes especiales?',
    answer:
      'No. Brócoli parte de alimentos cotidianos y de lo que ya tienes en casa, desde arroz, frijoles y huevos hasta frutas y vegetales.',
  },
  {
    question: '¿Funciona con supermercados de Honduras?',
    answer:
      'Sí. Brócoli contempla opciones disponibles en tiendas como Paiz, Walmart Honduras, La Colonia y Maxi Despensa.',
  },
  {
    question: '¿Cuándo estará disponible?',
    answer:
      'Estamos construyendo la primera versión. Puedes solicitar acceso anticipado y te avisaremos cuando abramos nuevos espacios.',
  },
]

function Brand() {
  return (
    <a className={styles.brand} href='#inicio' aria-label='Brócoli, inicio'>
      <Image
        className={styles.brandIcon}
        src='/brocoli.png'
        alt=''
        width={42}
        height={42}
        priority
      />
      <span>brócoli</span>
    </a>
  )
}

function Arrow() {
  return <span aria-hidden='true'>↗</span>
}

function PhoneShell({
  variant,
  className,
}: {
  variant: 'plan' | 'chat' | 'list'
  className?: string
}) {
  return (
    <div className={`${styles.phone} ${className ?? ''}`} aria-hidden='true'>
      <div className={styles.phoneTop}>
        <span>9:41</span>
        <span className={styles.dynamicIsland} />
        <span>•••</span>
      </div>

      {variant === 'plan' ? (
        <div className={styles.phoneScreen}>
          <div className={styles.appHeader}>
            <div>
              <p>Buenos días, Alex</p>
              <strong>Comidas para hoy.</strong>
            </div>
            <Image src='/brocoli.png' alt='' width={34} height={34} />
          </div>
          <div className={styles.progressCard}>
            <div className={styles.progressRing}>
              <svg viewBox='0 0 72 72' aria-hidden='true'>
                <defs>
                  <linearGradient
                    id='calorieProgress'
                    x1='8'
                    y1='62'
                    x2='62'
                    y2='8'
                    gradientUnits='userSpaceOnUse'
                  >
                    <stop stopColor='#78d91f' />
                    <stop offset='1' stopColor='#c1ff45' />
                  </linearGradient>
                </defs>
                <circle
                  className={styles.progressTrack}
                  cx='36'
                  cy='36'
                  r='28'
                />
                <circle
                  className={styles.progressArc}
                  cx='36'
                  cy='36'
                  r='28'
                  pathLength='100'
                />
              </svg>
              <div className={styles.progressValue}>
                <strong>64</strong>
                <span>%</span>
              </div>
            </div>
            <div className={styles.progressCopy}>
              <span className={styles.progressEyebrow}>Objetivo de hoy</span>
              <strong>
                1,240 <span>/ 1,940 kcal</span>
              </strong>
              <div className={styles.progressMeta}>
                <span>Vas muy bien</span>
                <small>700 kcal restantes</small>
              </div>
            </div>
          </div>
          <div className={styles.sectionTitle}>
            <strong>Comidas de hoy</strong>
            <span>Ver todo</span>
          </div>
          <div className={styles.mealCard}>
            <div className={styles.foodThumb}>
              <Image
                className={styles.mealPhoto}
                src='/meal-breakfast-greens-pexels.jpg'
                alt=''
                fill
                sizes='68px'
              />
              <span>07:30</span>
            </div>
            <div>
              <small>Desayuno</small>
              <strong>Huevos, tostada y hojas verdes</strong>
              <span>390 kcal · 22g proteína</span>
            </div>
          </div>
          <div className={styles.mealCard}>
            <div className={styles.foodThumb}>
              <Image
                className={styles.mealPhoto}
                src='/meal-chicken-rice-pexels.jpg'
                alt=''
                fill
                sizes='68px'
              />
              <span>12:30</span>
            </div>
            <div>
              <small>Almuerzo</small>
              <strong>Pollo, arroz y vegetales</strong>
              <span>610 kcal · 46g proteína</span>
            </div>
          </div>
          <div className={styles.tabBar}>
            <span className={styles.activeTab}>Hoy</span>
            <span>Plan</span>
            <span>Lista</span>
          </div>
        </div>
      ) : null}

      {variant === 'chat' ? (
        <div className={styles.phoneScreen}>
          <div className={styles.chatHeader}>
            <Image src='/brocoli.png' alt='' width={38} height={38} />
            <div>
              <strong>Brócoli</strong>
              <span>Comer saludable en casa</span>
            </div>
          </div>
          <div className={styles.chatDate}>HOY</div>
          <div className={`${styles.bubble} ${styles.botBubble}`}>
            ¿Qué ingredientes tienes para el almuerzo?
          </div>
          <div className={`${styles.bubble} ${styles.userBubble}`}>
            Pollo, arroz, brócoli y tomate.
          </div>
          <div className={`${styles.bubble} ${styles.botBubble}`}>
            Con eso puedes preparar pollo con arroz y vegetales. No necesitas
            comprar nada más.
          </div>
          <div className={styles.suggestion}>Ver receta →</div>
          <div className={styles.chatInput}>
            Escribe un mensaje… <span>↑</span>
          </div>
        </div>
      ) : null}

      {variant === 'list' ? (
        <div className={styles.phoneScreen}>
          <div className={styles.listHeader}>
            <span>Esta semana</span>
            <strong>Lista de compras</strong>
            <small>18 productos · aprox. L 1,460</small>
          </div>
          <div className={styles.storeRow}>
            <div>
              <small>Tienda cercana</small>
              <strong>Paiz · Tegucigalpa</strong>
            </div>
            <span>1.8 km</span>
          </div>
          {[
            ['Frutas y vegetales', '5 productos', 'Brócoli, banano, tomate…'],
            ['Proteínas', '4 productos', 'Pollo, huevos, yogur…'],
            ['Granos y despensa', '6 productos', 'Avena, arroz, almendras…'],
            ['Otros', '3 productos', 'Café, especias, limón'],
          ].map(([title, count, items], index) => (
            <div className={styles.listGroup} key={title}>
              <span className={index === 0 ? styles.checked : ''}>
                {index === 0 ? '✓' : ''}
              </span>
              <div>
                <strong>{title}</strong>
                <small>{items}</small>
              </div>
              <em>{count}</em>
            </div>
          ))}
          <div className={styles.phoneButton}>Empezar compra</div>
        </div>
      ) : null}

      <span className={styles.homeIndicator} />
    </div>
  )
}

export default function Home() {
  return (
    <main id='inicio'>
      <header className={styles.header}>
        <div className={styles.navbar}>
          <Brand />
          <nav className={styles.navLinks} aria-label='Navegación principal'>
            {navItems.map((item) => (
              <a key={item.href} href={item.href}>
                {item.label}
              </a>
            ))}
          </nav>
          <a className={styles.navCta} href='#acceso'>
            Acceso anticipado <Arrow />
          </a>
        </div>
      </header>

      <section className={styles.hero}>
        <h1>
          <span>Comer saludable empieza</span>
          <span>con lo que tienes en casa.</span>
        </h1>
        <p className={styles.heroCopy}>
          Levantate con energía por las mañanas. Brocoli arma tus planes de
          comida para que puedas levantarte cada día con energías y maximizes tu
          rendimiento.
        </p>
        <div className={styles.heroActions}>
          <a className={styles.primaryButton} href='#acceso'>
            Quiero comer mejor <Arrow />
          </a>
          <a className={styles.textLink} href='#como-funciona'>
            Conocer Brócoli <span aria-hidden='true'>↓</span>
          </a>
        </div>
        <div
          className={styles.storeBadges}
          aria-label='Próximamente en tiendas'
        >
          <a
            href='#acceso'
            aria-label='Acceder al acceso anticipado de Brócoli para App Store'
          >
            <Image
              src='/app-store-badge.svg'
              alt='Descárgalo en el App Store'
              width={150}
              height={50}
              unoptimized
            />
            <span>Acceder al acceso anticipado</span>
          </a>
          <a
            href='#acceso'
            aria-label='Acceder al acceso anticipado de Brócoli para Google Play'
          >
            <Image
              src='/google-play-badge.png'
              alt='Disponible en Google Play'
              width={169}
              height={50}
            />
            <span>Acceder al acceso anticipado</span>
          </a>
        </div>
        <div className={styles.proofLine}>
          <span>Ingredientes cotidianos</span>
          <i />
          <span>Comidas saludables</span>
          <i />
          <span>Menos desperdicio</span>
        </div>

        <div className={styles.phoneStage}>
          <div className={styles.stageGlow} />
          <PhoneShell variant='chat' className={styles.phoneLeft} />
          <PhoneShell variant='plan' className={styles.phoneCenter} />
          <PhoneShell variant='list' className={styles.phoneRight} />
        </div>
      </section>

      <section
        className={styles.retailerStrip}
        aria-label='Supermercados locales'
      >
        <p>Nos integramos con:</p>
        <div className={styles.storeLogos}>
          {localStores.map((store) => (
            <div
              className={`${styles.storeLogo} ${store.dark ? styles.storeLogoDark : ''}`}
              key={store.name}
            >
              <Image
                src={store.logo}
                alt={store.name}
                width={store.width}
                height={store.height}
                unoptimized
              />
            </div>
          ))}
        </div>
        <small>
          Ingredientes fáciles de encontrar cerca de casa y dentro de tu
          presupuesto.
        </small>
      </section>

      <section className={styles.manifesto}>
        <p>Comer bien empieza en tu cocina.</p>
        <h2>
          <span className={styles.manifestoLine}>
            Comidas saludables
            <span className={styles.countryName}>
              <span className={styles.hondurasMark} aria-hidden='true'>
                <i />
                <i />
                <i />
                <i />
                <i />
              </span>
              <span className={styles.countryWord}>hondureñas</span>
            </span>
          </span>
          <span className={styles.manifestoLine}>
            con ingredientes que ya tienes en casa.
          </span>
        </h2>
      </section>

      <section className={styles.benefits} id='producto'>
        <div className={styles.sectionIntro}>
          <p>Comer saludable con Brócoli</p>
          <h2>Todo empieza con lo que ya tienes en casa.</h2>
        </div>
        <div className={styles.benefitGrid}>
          {benefits.map((benefit) => (
            <article className={styles.benefitCard} key={benefit.number}>
              <span>{benefit.number}</span>
              <div className={styles.benefitImage}>
                <Image
                  src={benefit.image}
                  alt={benefit.alt}
                  fill
                  sizes='(max-width: 900px) 100vw, 33vw'
                />
              </div>
              <div>
                <h3>{benefit.title}</h3>
                <p>{benefit.copy}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.featureSection} id='como-funciona'>
        <div className={styles.featureVisual}>
          <div className={styles.miniNoteTop}>
            <span>Para esta semana</span>
            <strong>Comidas que dan energía</strong>
            <small>Ingredientes sencillos · porciones completas</small>
          </div>
          <PhoneShell variant='chat' className={styles.featurePhone} />
          <div className={styles.miniNoteBottom}>
            <span>Ya lo tienes en casa</span>
            <strong>Huevos, frijoles y aguacate</strong>
          </div>
        </div>
        <div className={styles.featureCopy}>
          <span className={styles.kicker}>01 — Tu cocina</span>
          <h2>Tu próxima comida empieza con lo que ya tienes.</h2>
          <p>
            Arroz, frijoles, huevos, pollo o vegetales: ingredientes normales
            pueden convertirse en comidas saludables, ricas y completas.
          </p>
          <ul>
            <li>
              <span>✓</span> Ingredientes de todos los días
            </li>
            <li>
              <span>✓</span> Comidas hondureñas y variadas
            </li>
            <li>
              <span>✓</span> Opciones para cada presupuesto
            </li>
          </ul>
        </div>
      </section>

      <section className={`${styles.featureSection} ${styles.reverseFeature}`}>
        <div className={styles.featureCopy}>
          <span className={styles.kicker}>02 — Lo que falta</span>
          <h2>Completa tu semana comprando solo lo necesario.</h2>
          <p>
            Aprovecha primero lo que tienes en casa y completa tus comidas con
            productos fáciles de encontrar dentro de tu presupuesto.
          </p>
          <a className={styles.inlineLink} href='#acceso'>
            Quiero probar Brócoli <Arrow />
          </a>
        </div>
        <div className={`${styles.featureVisual} ${styles.listVisual}`}>
          <div className={styles.priceChip}>Solo lo que hace falta</div>
          <PhoneShell variant='list' className={styles.featurePhone} />
        </div>
      </section>

      <section className={styles.stepsSection}>
        <div className={styles.stepsHeader}>
          <span>Comer saludable con Brócoli</span>
          <h2>Empieza en tu cocina.</h2>
        </div>
        <div className={styles.stepsGrid}>
          <article>
            <span>01</span>
            <h3>Mira lo que tienes</h3>
            <p>Empieza con ingredientes que ya están en tu cocina.</p>
          </article>
          <article>
            <span>02</span>
            <h3>Come rico y variado</h3>
            <p>Prepara comidas saludables que sí quieres comer.</p>
          </article>
          <article>
            <span>03</span>
            <h3>Compra solo lo que falta</h3>
            <p>Completa la semana sin gastar de más ni desperdiciar comida.</p>
          </article>
        </div>
      </section>

      <section className={styles.faqSection} id='preguntas'>
        <div className={styles.faqHeading}>
          <span>Preguntas frecuentes</span>
          <h2>Comer saludable, sin complicarlo.</h2>
          <p>Lo esencial antes de probar Brócoli.</p>
        </div>
        <div className={styles.faqList}>
          {faqs.map((faq) => (
            <details key={faq.question}>
              <summary>
                {faq.question}
                <span aria-hidden='true'>+</span>
              </summary>
              <p>{faq.answer}</p>
            </details>
          ))}
        </div>
      </section>

      <section className={styles.ctaSection} id='acceso'>
        <Image
          src='/brocoli.png'
          alt='Logo de Brócoli'
          width={86}
          height={86}
        />
        <span>Brócoli llega pronto.</span>
        <h2>Únete a la familia Brócoli.</h2>
        <p>Déjanos tu correo y sé de las primeras personas en probarlo.</p>
        <form className={styles.signupForm}>
          <label className={styles.srOnly} htmlFor='email'>
            Correo electrónico
          </label>
          <input
            id='email'
            name='email'
            type='email'
            placeholder='tu@correo.com'
            autoComplete='email'
            required
          />
          <button type='submit'>
            Solicitar acceso <Arrow />
          </button>
        </form>
      </section>

      <footer className={styles.footer}>
        <div className={styles.footerMain}>
          <div className={styles.footerBrand}>
            <Brand />
            <p>Comer saludable con lo que tienes en casa.</p>
          </div>

          <nav className={styles.footerColumn} aria-label='Enlaces legales'>
            <h2>Legal</h2>
            <a href='/politica-de-privacidad'>Política de privacidad</a>
            <a href='/terminos-de-uso'>Términos de uso</a>
            <a href='/politica-de-cookies'>Política de cookies</a>
          </nav>

          <nav className={styles.footerColumn} aria-label='Enlaces de Brócoli'>
            <h2>Brócoli</h2>
            <a href='#preguntas'>Preguntas frecuentes</a>
            <a href='#como-funciona'>Conocer Brócoli</a>
            <a href='#acceso'>Contacto</a>
            <a href='#acceso'>Acceso anticipado</a>
          </nav>
        </div>
        <div className={styles.footerBottom}>
          <span>© 2026 Brócoli</span>
          <span>Hecho en Honduras para comer saludable.</span>
          <span>Desarrollado por DelCraft AI</span>
        </div>
      </footer>
    </main>
  )
}
