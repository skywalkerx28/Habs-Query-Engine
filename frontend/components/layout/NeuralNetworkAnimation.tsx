'use client'

import { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'

interface NeuralNetworkAnimationProps {
  className?: string
}

interface ParticleData {
  velocity: THREE.Vector3
  numConnections: number
  type?: 'faceoff' | 'pass' | 'shot' | 'save' | 'goal' | 'hit' | 'takeaway' | 'penalty' | 'period' | 'player'
  label?: string
  id?: string
  relatedTo?: string[]
  timestamp?: number  // Game time in seconds
  period?: number
  sequence?: number  // Order in the event chain
}

// Simple OrbitControls implementation
class SimpleOrbitControls {
  camera: THREE.PerspectiveCamera
  domElement: HTMLElement
  target = new THREE.Vector3()
  
  spherical = new THREE.Spherical()
  sphericalDelta = new THREE.Spherical()
  
  scale = 1
  panOffset = new THREE.Vector3()
  zoomChanged = false
  
  rotateSpeed = 1.0
  zoomSpeed = 1.2
  
  mouseButtons = { LEFT: 0, MIDDLE: 1, RIGHT: 2 }
  
  private rotateStart = new THREE.Vector2()
  private rotateEnd = new THREE.Vector2()
  private rotateDelta = new THREE.Vector2()
  
  private isMouseDown = false
  
  // Store bound functions for cleanup
  private boundOnMouseDown: (e: MouseEvent) => void
  private boundOnMouseMove: (e: MouseEvent) => void
  private boundOnMouseUp: (e: MouseEvent) => void
  private boundOnMouseWheel: (e: WheelEvent) => void
  
  constructor(camera: THREE.PerspectiveCamera, domElement: HTMLElement) {
    this.camera = camera
    this.domElement = domElement
    
    // Bind methods and store references
    this.boundOnMouseDown = this.onMouseDown.bind(this)
    this.boundOnMouseMove = this.onMouseMove.bind(this)
    this.boundOnMouseUp = this.onMouseUp.bind(this)
    this.boundOnMouseWheel = this.onMouseWheel.bind(this)
    
    // Add event listeners
    this.domElement.addEventListener('mousedown', this.boundOnMouseDown)
    this.domElement.addEventListener('mousemove', this.boundOnMouseMove)
    this.domElement.addEventListener('mouseup', this.boundOnMouseUp)
    this.domElement.addEventListener('mouseleave', this.boundOnMouseUp)
    this.domElement.addEventListener('wheel', this.boundOnMouseWheel, { passive: false })
    this.domElement.addEventListener('contextmenu', (e) => e.preventDefault())
    
    this.update()
  }
  
  onMouseDown(event: MouseEvent) {
    event.preventDefault()
    event.stopPropagation()
    this.isMouseDown = true
    this.rotateStart.set(event.clientX, event.clientY)
    console.log('Mouse down at:', event.clientX, event.clientY)
  }
  
  onMouseMove(event: MouseEvent) {
    if (!this.isMouseDown) return
    
    event.preventDefault()
    event.stopPropagation()
    
    this.rotateEnd.set(event.clientX, event.clientY)
    this.rotateDelta.subVectors(this.rotateEnd, this.rotateStart).multiplyScalar(this.rotateSpeed)
    
    const element = this.domElement
    this.rotateLeft(2 * Math.PI * this.rotateDelta.x / element.clientHeight)
    this.rotateUp(2 * Math.PI * this.rotateDelta.y / element.clientHeight)
    
    this.rotateStart.copy(this.rotateEnd)
    this.update()
  }
  
  onMouseUp(event: MouseEvent) {
    event.preventDefault()
    this.isMouseDown = false
  }
  
  onMouseWheel(event: WheelEvent) {
    event.preventDefault()
    event.stopPropagation()
    
    if (event.deltaY < 0) {
      this.dollyIn(this.getZoomScale())
    } else if (event.deltaY > 0) {
      this.dollyOut(this.getZoomScale())
    }
    
    this.update()
  }
  
  getZoomScale() {
    return Math.pow(0.95, this.zoomSpeed)
  }
  
  rotateLeft(angle: number) {
    this.sphericalDelta.theta -= angle
  }
  
  rotateUp(angle: number) {
    this.sphericalDelta.phi -= angle
  }
  
  dollyIn(dollyScale: number) {
    this.scale /= dollyScale
  }
  
  dollyOut(dollyScale: number) {
    this.scale *= dollyScale
  }
  
  update() {
    const offset = new THREE.Vector3()
    const quat = new THREE.Quaternion().setFromUnitVectors(
      this.camera.up,
      new THREE.Vector3(0, 1, 0)
    )
    const quatInverse = quat.clone().invert()
    
    const position = this.camera.position
    
    offset.copy(position).sub(this.target)
    offset.applyQuaternion(quat)
    
    this.spherical.setFromVector3(offset)
    
    this.spherical.theta += this.sphericalDelta.theta
    this.spherical.phi += this.sphericalDelta.phi
    
    this.spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, this.spherical.phi))
    
    this.spherical.radius *= this.scale
    this.spherical.radius = Math.max(400, Math.min(2000, this.spherical.radius))
    
    this.target.add(this.panOffset)
    
    offset.setFromSpherical(this.spherical)
    offset.applyQuaternion(quatInverse)
    
    position.copy(this.target).add(offset)
    
    this.camera.lookAt(this.target)
    
    this.sphericalDelta.set(0, 0, 0)
    this.panOffset.set(0, 0, 0)
    
    this.scale = 1
  }
  
  dispose() {
    this.domElement.removeEventListener('mousedown', this.boundOnMouseDown)
    this.domElement.removeEventListener('mousemove', this.boundOnMouseMove)
    this.domElement.removeEventListener('mouseup', this.boundOnMouseUp)
    this.domElement.removeEventListener('mouseleave', this.boundOnMouseUp)
    this.domElement.removeEventListener('wheel', this.boundOnMouseWheel)
  }
}

export function NeuralNetworkAnimation({ className = '' }: NeuralNetworkAnimationProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const labelsContainerRef = useRef<HTMLDivElement>(null)
  const [badges, setBadges] = useState<Array<{
    id: string
    x: number
    y: number
    type: string
    label: string
    visible: boolean
  }>>([])
  
  const sceneRef = useRef<{
    scene?: THREE.Scene
    camera?: THREE.PerspectiveCamera
    renderer?: THREE.WebGLRenderer
    particles?: THREE.BufferGeometry
    pointCloud?: THREE.Points
    linesMesh?: THREE.LineSegments
    particlesData?: ParticleData[]
    particlePositions?: Float32Array
    positions?: Float32Array
    colors?: Float32Array
    animationId?: number
    controls?: SimpleOrbitControls
  }>({})

  useEffect(() => {
    if (!containerRef.current) return

    const container = containerRef.current
    const scene = sceneRef.current

    // Constants
    const maxParticleCount = 300
    const particleCount = 150
    const r = 600
    const rHalf = r / 2
    const minDistance = 150

    // Initialize scene
    scene.scene = new THREE.Scene()
    scene.camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 1, 4000)
    scene.camera.position.z = 1200

    scene.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    scene.renderer.setPixelRatio(window.devicePixelRatio)
    scene.renderer.setSize(container.clientWidth, container.clientHeight)
    scene.renderer.setClearColor(0x000000, 0) // Transparent background
    scene.renderer.domElement.style.position = 'absolute'
    scene.renderer.domElement.style.top = '0'
    scene.renderer.domElement.style.left = '0'
    scene.renderer.domElement.style.width = '100%'
    scene.renderer.domElement.style.height = '100%'
    container.appendChild(scene.renderer.domElement)

    // Add orbit controls
    scene.controls = new SimpleOrbitControls(scene.camera, scene.renderer.domElement)
    console.log('OrbitControls initialized')

    // Create particle system
    const segments = maxParticleCount * maxParticleCount
    scene.positions = new Float32Array(segments * 3)
    scene.colors = new Float32Array(segments * 3)

    // Particle material - military style white/gray
    const pMaterial = new THREE.PointsMaterial({
      color: 0xFFFFFF,
      size: 2,
      blending: THREE.AdditiveBlending,
      transparent: true,
      sizeAttenuation: false,
      opacity: 0.8
    })

    scene.particles = new THREE.BufferGeometry()
    scene.particlePositions = new Float32Array(maxParticleCount * 3)
    scene.particlesData = []

    // Single game: MTL vs TOR - with realistic event sequence
    const gameEvents = [
      // Period 1 Start
      { type: 'period', label: 'Period 1', sequence: 0, period: 1, timestamp: 0 },
      
      // First sequence leading to a goal
      { type: 'faceoff', label: 'Faceoff Win - Suzuki', sequence: 1, period: 1, timestamp: 15 },
      { type: 'pass', label: 'Pass - Suzuki to Caufield', sequence: 2, period: 1, timestamp: 18 },
      { type: 'shot', label: 'Shot - Caufield', sequence: 3, period: 1, timestamp: 20 },
      { type: 'save', label: 'Save - Samsonov', sequence: 4, period: 1, timestamp: 21 },
      
      // Defensive play
      { type: 'hit', label: 'Hit - Matheson on Matthews', sequence: 5, period: 1, timestamp: 45 },
      { type: 'takeaway', label: 'Takeaway - Dach', sequence: 6, period: 1, timestamp: 47 },
      { type: 'pass', label: 'Breakout Pass - Dach', sequence: 7, period: 1, timestamp: 50 },
      
      // Goal sequence
      { type: 'pass', label: 'Pass - Matheson to Suzuki', sequence: 8, period: 1, timestamp: 240 },
      { type: 'pass', label: 'Pass - Suzuki to Caufield', sequence: 9, period: 1, timestamp: 243 },
      { type: 'shot', label: 'Shot - Caufield', sequence: 10, period: 1, timestamp: 245 },
      { type: 'goal', label: 'GOAL! Caufield (Suzuki, Matheson)', sequence: 11, period: 1, timestamp: 246 },
      
      // Period 2
      { type: 'period', label: 'Period 2', sequence: 12, period: 2, timestamp: 1200 },
      
      // Penalty sequence
      { type: 'hit', label: 'Hit - Xhekaj on Marner', sequence: 13, period: 2, timestamp: 1350 },
      { type: 'penalty', label: 'Penalty - Xhekaj (Roughing)', sequence: 14, period: 2, timestamp: 1351 },
      
      // Power play defense
      { type: 'faceoff', label: 'PK Faceoff Win - Dvorak', sequence: 15, period: 2, timestamp: 1360 },
      { type: 'pass', label: 'Clear - Matheson', sequence: 16, period: 2, timestamp: 1365 },
      
      // Players involved
      { type: 'player', label: 'Suzuki #14', sequence: 100 },
      { type: 'player', label: 'Caufield #22', sequence: 101 },
      { type: 'player', label: 'Matheson #8', sequence: 102 },
      { type: 'player', label: 'Dach #77', sequence: 103 },
    ]

    // Initialize particles with game events
    for (let i = 0; i < maxParticleCount; i++) {
      // Position particles in a timeline-like arrangement
      let x, y, z
      
      if (i < gameEvents.length) {
        // Arrange events in a spiral pattern based on sequence
        const event = gameEvents[i]
        const angle = (event.sequence / 20) * Math.PI * 2
        const radius = 200 + (event.sequence * 10)
        
        x = Math.cos(angle) * radius
        y = (event.period ? (event.period - 2) * 150 : 0) + (Math.random() * 50 - 25)
        z = Math.sin(angle) * radius
      } else {
        // Random positions for other particles
        x = Math.random() * r - r / 2
        y = Math.random() * r - r / 2
        z = Math.random() * r - r / 2
      }

      scene.particlePositions[i * 3] = x
      scene.particlePositions[i * 3 + 1] = y
      scene.particlePositions[i * 3 + 2] = z

      const particleData: ParticleData = {
        velocity: new THREE.Vector3(
          -0.2 + Math.random() * 0.4,
          -0.2 + Math.random() * 0.4,
          -0.2 + Math.random() * 0.4
        ),
        numConnections: 0
      }

      // Assign game event data
      if (i < gameEvents.length) {
        const event = gameEvents[i]
        particleData.type = event.type as any
        particleData.label = event.label
        particleData.id = `event-${i}`
        particleData.sequence = event.sequence
        particleData.period = event.period
        particleData.timestamp = event.timestamp
        
        // Connect events in sequence
        if (i > 0 && event.sequence > 0 && event.sequence < 100) {
          // Connect to previous event in sequence
          particleData.relatedTo = [`event-${i - 1}`]
          
          // Special connections for goals
          if (event.type === 'goal') {
            // Connect to assists (previous 2 events)
            particleData.relatedTo = [`event-${i - 1}`, `event-${i - 2}`, `event-${i - 3}`]
          }
          
          // Connect players to their events
          if (event.label?.includes('Suzuki')) {
            particleData.relatedTo = [...(particleData.relatedTo || []), 'event-17']
          }
          if (event.label?.includes('Caufield')) {
            particleData.relatedTo = [...(particleData.relatedTo || []), 'event-18']
          }
          if (event.label?.includes('Matheson')) {
            particleData.relatedTo = [...(particleData.relatedTo || []), 'event-19']
          }
          if (event.label?.includes('Dach')) {
            particleData.relatedTo = [...(particleData.relatedTo || []), 'event-20']
          }
        }
      }

      scene.particlesData.push(particleData)
    }

    scene.particles.setDrawRange(0, particleCount)
    scene.particles.setAttribute('position', new THREE.BufferAttribute(scene.particlePositions, 3).setUsage(THREE.DynamicDrawUsage))

    scene.pointCloud = new THREE.Points(scene.particles, pMaterial)
    scene.scene.add(scene.pointCloud)

    // Create line system
    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute('position', new THREE.BufferAttribute(scene.positions, 3).setUsage(THREE.DynamicDrawUsage))
    geometry.setAttribute('color', new THREE.BufferAttribute(scene.colors, 3).setUsage(THREE.DynamicDrawUsage))
    geometry.computeBoundingSphere()
    geometry.setDrawRange(0, 0)

    // Line material - military style
    const material = new THREE.LineBasicMaterial({
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      transparent: true,
      opacity: 0.3
    })

    scene.linesMesh = new THREE.LineSegments(geometry, material)
    scene.scene.add(scene.linesMesh)

    // Animation loop
    const animate = () => {
      let vertexpos = 0
      let colorpos = 0
      let numConnected = 0

      // Reset connections
      for (let i = 0; i < particleCount; i++) {
        scene.particlesData![i].numConnections = 0
      }

      // Update particles and create connections
      for (let i = 0; i < particleCount; i++) {
        const particleData = scene.particlesData![i]

        // Update positions
        scene.particlePositions![i * 3] += particleData.velocity.x
        scene.particlePositions![i * 3 + 1] += particleData.velocity.y
        scene.particlePositions![i * 3 + 2] += particleData.velocity.z

        // Boundary collision
        if (scene.particlePositions![i * 3 + 1] < -rHalf || scene.particlePositions![i * 3 + 1] > rHalf) {
          particleData.velocity.y = -particleData.velocity.y
        }
        if (scene.particlePositions![i * 3] < -rHalf || scene.particlePositions![i * 3] > rHalf) {
          particleData.velocity.x = -particleData.velocity.x
        }
        if (scene.particlePositions![i * 3 + 2] < -rHalf || scene.particlePositions![i * 3 + 2] > rHalf) {
          particleData.velocity.z = -particleData.velocity.z
        }

        // Check connections to other particles
        for (let j = i + 1; j < particleCount; j++) {
          const particleDataB = scene.particlesData![j]

          const dx = scene.particlePositions![i * 3] - scene.particlePositions![j * 3]
          const dy = scene.particlePositions![i * 3 + 1] - scene.particlePositions![j * 3 + 1]
          const dz = scene.particlePositions![i * 3 + 2] - scene.particlePositions![j * 3 + 2]
          const dist = Math.sqrt(dx * dx + dy * dy + dz * dz)

          // Check if particles are related (stronger connection)
          const areRelated = 
            (particleData.id && particleDataB.relatedTo?.includes(particleData.id)) ||
            (particleDataB.id && particleData.relatedTo?.includes(particleDataB.id))
          
          // Use larger distance for related particles, normal for others
          const connectionDistance = areRelated ? minDistance * 2 : minDistance

          if (dist < connectionDistance) {
            particleData.numConnections++
            particleDataB.numConnections++

            // Stronger alpha for related particles
            const alpha = areRelated 
              ? Math.min(1.0, (1.0 - dist / connectionDistance) * 1.2)
              : (1.0 - dist / connectionDistance) * 0.6

            // Line vertices
            scene.positions![vertexpos++] = scene.particlePositions![i * 3]
            scene.positions![vertexpos++] = scene.particlePositions![i * 3 + 1]
            scene.positions![vertexpos++] = scene.particlePositions![i * 3 + 2]

            scene.positions![vertexpos++] = scene.particlePositions![j * 3]
            scene.positions![vertexpos++] = scene.particlePositions![j * 3 + 1]
            scene.positions![vertexpos++] = scene.particlePositions![j * 3 + 2]

            // Line colors - military white/gray
            scene.colors![colorpos++] = alpha
            scene.colors![colorpos++] = alpha
            scene.colors![colorpos++] = alpha

            scene.colors![colorpos++] = alpha
            scene.colors![colorpos++] = alpha
            scene.colors![colorpos++] = alpha

            numConnected++
          }
        }
      }

      // Update geometries
      scene.linesMesh!.geometry.setDrawRange(0, numConnected * 2)
      scene.linesMesh!.geometry.attributes.position.needsUpdate = true
      scene.linesMesh!.geometry.attributes.color.needsUpdate = true
      scene.pointCloud!.geometry.attributes.position.needsUpdate = true

      // Update controls
      if (scene.controls) {
        scene.controls.update()
      }

      // Update badge positions
      const tempBadges: typeof badges = []
      for (let i = 0; i < particleCount && i < 21; i++) {  // Show first 21 events (includes players)
        const particleData = scene.particlesData![i]
        if (particleData.type && particleData.label) {
          const vector = new THREE.Vector3(
            scene.particlePositions![i * 3],
            scene.particlePositions![i * 3 + 1],
            scene.particlePositions![i * 3 + 2]
          )
          
          // Project 3D position to 2D screen coordinates
          vector.project(scene.camera!)
          
          const x = (vector.x * 0.5 + 0.5) * container.clientWidth
          const y = (-(vector.y * 0.5) + 0.5) * container.clientHeight
          
          tempBadges.push({
            id: particleData.id || `particle-${i}`,
            x,
            y,
            type: particleData.type,
            label: particleData.label,
            visible: vector.z < 1 // Only show if in front of camera
          })
        }
      }
      setBadges(tempBadges)

      scene.renderer!.render(scene.scene!, scene.camera!)
      scene.animationId = requestAnimationFrame(animate)
    }

    animate()

    // Handle resize
    const handleResize = () => {
      if (!container || !scene.camera || !scene.renderer) return
      
      scene.camera.aspect = container.clientWidth / container.clientHeight
      scene.camera.updateProjectionMatrix()
      scene.renderer.setSize(container.clientWidth, container.clientHeight)
    }

    window.addEventListener('resize', handleResize)

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
      
      if (scene.animationId) {
        cancelAnimationFrame(scene.animationId)
      }
      
      if (scene.controls) {
        scene.controls.dispose()
      }
      
      if (scene.renderer && container.contains(scene.renderer.domElement)) {
        container.removeChild(scene.renderer.domElement)
      }
      
      // Dispose Three.js resources
      scene.particles?.dispose()
      scene.linesMesh?.geometry.dispose()
      if (scene.pointCloud?.material) {
        if (Array.isArray(scene.pointCloud.material)) {
          scene.pointCloud.material.forEach(m => m.dispose())
        } else {
          scene.pointCloud.material.dispose()
        }
      }
      if (scene.linesMesh?.material) {
        if (Array.isArray(scene.linesMesh.material)) {
          scene.linesMesh.material.forEach(m => m.dispose())
        } else {
          scene.linesMesh.material.dispose()
        }
      }
      scene.renderer?.dispose()
      
      // Clear references
      sceneRef.current = {}
    }
  }, [])

  return (
    <div className="relative w-full h-full">
      <div 
        ref={containerRef}
        className={`relative w-full h-full cursor-grab active:cursor-grabbing ${className}`}
        style={{ minHeight: '500px' }}
        title="Click and drag to rotate • Scroll to zoom"
      />
      
      {/* Badge overlays */}
      <div className="absolute inset-0 pointer-events-none" ref={labelsContainerRef}>
        {badges.map((badge) => badge.visible && (
          <div
            key={badge.id}
            className="absolute transform -translate-x-1/2 -translate-y-1/2 pointer-events-auto"
            style={{
              left: `${badge.x}px`,
              top: `${badge.y}px`,
              zIndex: 100
            }}
          >
            <div className={`
              px-2 py-1 rounded-full text-xs font-military-display
              backdrop-blur-sm border animate-pulse
              ${badge.type === 'period' ? 'bg-black border-white text-white font-bold' : ''}
              ${badge.type === 'faceoff' ? 'bg-gray-900/90 border-gray-400 text-gray-200' : ''}
              ${badge.type === 'pass' ? 'bg-gray-800/90 border-gray-500 text-gray-100' : ''}
              ${badge.type === 'shot' ? 'bg-gray-700/90 border-white text-white' : ''}
              ${badge.type === 'save' ? 'bg-gray-900/90 border-gray-300 text-gray-200' : ''}
              ${badge.type === 'goal' ? 'bg-red-900/90 border-red-500 text-white font-bold' : ''}
              ${badge.type === 'hit' ? 'bg-black/90 border-gray-500 text-gray-100' : ''}
              ${badge.type === 'takeaway' ? 'bg-gray-800/90 border-gray-400 text-gray-200' : ''}
              ${badge.type === 'penalty' ? 'bg-red-800/90 border-red-600 text-red-100' : ''}
              ${badge.type === 'player' ? 'bg-white/90 border-black text-black font-bold' : ''}
              hover:scale-110 transition-transform cursor-pointer
            `}>
              {badge.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
