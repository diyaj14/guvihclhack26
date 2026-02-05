"use client";

import React, { useState, useEffect, useRef } from 'react';
import {
    Shield, Brain, Zap, Activity, Volume2,
    Search, Bell, Settings, ChevronRight,
    Clock, Database, ArrowRight, User,
    Layout, MessageSquare, Calendar, Folder,
    Maximize2, TrendingUp, DollarSign, Timer,
    Info, HelpCircle, ShieldAlert, CheckCircle,
    Plus, Users, Lock, Radio, MousePointer2,
    Cpu, Server, Terminal, Layers, Globe,
    Send, RefreshCw, UserCircle, ShieldCheck,
    Phone, PhoneOff, Mic, MicOff, ChevronLeft
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import * as LivekitClient from 'livekit-client';

// --- Types ---
interface Message {
    id?: string;
    role: 'agent' | 'scammer';
    text: string;
    timestamp: string;
    source?: 'voice' | 'text';
}

interface Intelligence {
    scammerName: string[];
    bankAccounts: string[];
    upiIds: string[];
    phishingLinks: string[];
    phoneNumbers: string[];
    location: string[];
    jobTitle: string[];
}

// --- Constants ---
const LIVEKIT_URL = "wss://vigilante-nk6tbkbt.livekit.cloud";
const TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiU2NhbW1lciBDYWxsZXIiLCJ2aWRlbyI6eyJyb29tSm9pbiI6dHJ1ZSwicm9vbSI6InRlc3Qtcm9vbSIsImNhblB1Ymxpc2giOnRydWUsImNhblN1YnNjcmliZSI6dHJ1ZSwiY2FuUHVibGlzaERhdGEiOnRydWUsImNhblVwZGF0ZU93bk1ldGFkYXRhIjp0cnVlfSwic3ViIjoic2NhbW1lcl9pZGVudGl0eSIsImlzcyI6IkFQSWM4Wjg4TXVqeG9ZdSIsIm5iZiI6MTc3MDMwNjY4MCwiZXhwIjoxNzcwMzI4MjgwfQ.DS_gdwM48JifkoWBHI5MhDJtdH7UEjL0bdUOfu7cdOc";

// --- Sub-Components ---

const CircularGauge = ({ value, label, active = false }: { value: number, label: string, active?: boolean }) => {
    const radius = 70;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (value / 100) * circumference;

    return (
        <div className={`flex flex-col items-center justify-center bg-white/40 backdrop-blur-xl rounded-[2.5rem] border transition-all duration-500 ${active ? 'border-rose-400 shadow-[0_0_40px_rgba(244,63,94,0.3)] scale-[1.02]' : 'border-white shadow-xl'} p-8 h-full relative overflow-hidden group`}>
            {active && <div className="absolute inset-0 bg-rose-500/5 animate-pulse rounded-[2.5rem]" />}
            <div className="absolute top-6 left-0 right-0 text-center">
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{label}</span>
            </div>

            <div className="relative w-48 h-48 flex items-center justify-center mt-4">
                {/* Background Track */}
                <svg className="transform -rotate-90 w-full h-full">
                    <circle
                        cx="50%"
                        cy="50%"
                        r={radius}
                        stroke="#e2e8f0"
                        strokeWidth="12"
                        fill="transparent"
                        className="opacity-50"
                    />
                    {/* Foreground Progress - Added Gradient Definition */}
                    <defs>
                        <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#6366f1" />
                            <stop offset="100%" stopColor="#f43f5e" />
                        </linearGradient>
                    </defs>
                    <motion.circle
                        cx="50%"
                        cy="50%"
                        r={radius}
                        stroke="url(#gaugeGradient)"
                        strokeWidth="12"
                        fill="transparent"
                        strokeDasharray={circumference}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        strokeLinecap="round"
                    />
                </svg>

                {/* Center Value */}
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-5xl font-black text-slate-800 tracking-tighter drop-shadow-sm">{Math.floor(value)}%</span>
                    <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest mt-1">Intensity</span>
                </div>
            </div>
        </div>
    );
};

const FatigueThermometer = ({ value, active = false }: { value: number, active?: boolean }) => (
    <div className={`flex flex-col items-center bg-white/40 backdrop-blur-xl rounded-[2.5rem] border transition-all duration-500 ${active ? 'border-rose-400 shadow-[0_0_30px_rgba(244,63,94,0.2)]' : 'border-white shadow-xl'} p-8 h-full relative overflow-hidden`}>
        <div className="absolute top-4 right-6 text-[8px] font-black text-slate-300 uppercase tracking-widest">Scammer Fatigue</div>
        <div className="flex-1 w-8 bg-slate-100 rounded-full relative mb-4 mt-6 border border-slate-200 overflow-hidden">
            <motion.div
                className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-indigo-500 via-purple-500 to-rose-500 rounded-full"
                initial={{ height: 0 }}
                animate={{ height: `${value}%` }}
                transition={{ duration: 1 }}
            />
            {active && (
                <motion.div
                    animate={{ opacity: [0, 1, 0] }}
                    transition={{ repeat: Infinity, duration: 1 }}
                    className="absolute inset-0 bg-white/20"
                />
            )}
        </div>
        <span className="text-xl font-black text-slate-800 tracking-tighter">{value}%</span>
    </div>
);

const MoneyGraph = ({ data, current }: { data: number[], current: number }) => {
    // Only take last 20 points
    const pointsData = data.slice(-20);
    // Ensure we have at least 2 points for a line
    const safeData = pointsData.length < 2 ? [0, current] : pointsData;

    const max = Math.max(...safeData, current * 1.2, 5000);
    const min = 0;
    const height = 40;
    const width = 200;

    // Create points for SVG path
    const points = safeData.map((val, i, arr) => {
        const x = (i / (arr.length - 1 || 1)) * width;
        const y = height - ((val - min) / (max - min)) * height;
        return `${x},${y}`;
    }).join(' ');

    return (
        <div className={`bg-white/40 backdrop-blur-xl rounded-[2.5rem] border transition-all duration-500 ${current > 0 ? 'border-emerald-400 shadow-[0_0_30px_rgba(16,185,129,0.1)]' : 'border-white shadow-xl'} p-8 flex flex-col justify-between h-full relative overflow-hidden`}>
            <div className="absolute top-4 right-6 text-[8px] font-black text-slate-300 uppercase tracking-widest">Money Saved</div>
            <div className="z-10 mt-2">
                <div className="flex items-baseline gap-2">
                    <span className="text-4xl font-black text-emerald-600 tracking-tighter">₹{current.toLocaleString()}</span>
                    <span className="text-[10px] font-black text-slate-400 uppercase">Estimated</span>
                </div>
            </div>

            {/* Graph Container */}
            <div className="absolute bottom-0 left-0 right-0 h-16 opacity-50 pointer-events-none">
                <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
                    <defs>
                        <linearGradient id="moneyGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#10b981" stopOpacity="0.4" />
                            <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
                        </linearGradient>
                    </defs>
                    <path
                        d={`M 0,${height} ${points ? 'L ' + points : ''} L ${width},${height} Z`}
                        fill="url(#moneyGradient)"
                    />
                    <path
                        d={`M 0,${height} ${points ? 'L ' + points : ''}`}
                        fill="none"
                        stroke="#10b981"
                        strokeWidth="2"
                    />
                </svg>
            </div>
        </div>
    );
};

const LatencySparkline = ({ data }: { data: number[] }) => (
    <div className="bg-white/40 backdrop-blur-xl rounded-[2.5rem] border border-white shadow-xl p-8 flex flex-col gap-4 relative">
        <div className="absolute top-4 right-6 text-[8px] font-black text-slate-300 uppercase tracking-widest">Latency (ms)</div>
        <div className="flex items-end gap-1 h-24 mt-4">
            {data.map((v, i) => (
                <motion.div
                    key={i}
                    initial={{ height: 0 }}
                    animate={{ height: `${Math.min((v / 1000) * 100, 100)}%` }}
                    className="flex-1 bg-indigo-500/20 rounded-t-sm border-t-2 border-indigo-500"
                />
            ))}
            {data.length === 0 && <div className="flex-1 flex items-center justify-center text-[10px] font-black text-slate-300 uppercase italic">Awaiting Ping...</div>}
        </div>
        <div className="flex justify-between items-baseline">
            <span className="text-2xl font-black text-slate-800 tracking-tighter">{data[data.length - 1] || 0}</span>
            <span className="text-[10px] font-black text-slate-400 uppercase">Avg: {data.length > 0 ? Math.floor(data.reduce((a, b) => a + b, 0) / data.length) : 0}ms</span>
        </div>
    </div>
);

const PersonaCard = ({ name, role, active, onClick, avatar }: { name: string, role: string, active: boolean, onClick: () => void, avatar: string }) => (
    <button
        onClick={onClick}
        className={`flex items-center gap-4 p-4 rounded-3xl transition-all border-2 ${active ? 'bg-indigo-600 border-indigo-600 shadow-xl shadow-indigo-600/20' : 'bg-white border-transparent hover:bg-slate-50'}`}
    >
        <div className="w-12 h-12 rounded-2xl overflow-hidden border-2 border-white/20">
            <img src={avatar} alt={name} className="w-full h-full object-cover" />
        </div>
        <div className="text-left">
            <h4 className={`text-sm font-black tracking-tight ${active ? 'text-white' : 'text-slate-800'}`}>{name}</h4>
            <p className={`text-[10px] font-bold uppercase tracking-widest ${active ? 'text-white/60' : 'text-slate-400'}`}>{role}</p>
        </div>
    </button>
);

export default function ConsolePage() {
    const [mounted, setMounted] = useState(false);
    const [persona, setPersona] = useState<'grandma' | 'ramesh'>('grandma');
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const [logs, setLogs] = useState<string[]>(["[00:00:01] PROTOCOL INITIALIZED :: VERSION 2.5", "[00:00:02] AWAITING UPLINK..."]);
    const [intel, setIntel] = useState<Intelligence>({
        scammerName: [], bankAccounts: [], upiIds: [], phishingLinks: [], phoneNumbers: [], location: [], jobTitle: []
    });
    const [metrics, setMetrics] = useState({
        threatLevel: 0,
        fatigue: 0,
        timeWasted: "0m 00s",
        moneySaved: 0,
        moneyHistory: [0] as number[],
        latencyHistory: [] as number[]
    });

    // Voice State
    const [isVoiceConnected, setIsVoiceConnected] = useState(false);
    const [isMuted, setIsMuted] = useState(false);
    const [room, setRoom] = useState<LivekitClient.Room | null>(null);
    const [isAgentSpeaking, setIsAgentSpeaking] = useState(false);
    const [isUserSpeaking, setIsUserSpeaking] = useState(false);

    const chatEndRef = useRef<HTMLDivElement>(null);
    const startTimeRef = useRef<number>(Date.now());
    const audioContextRef = useRef<AudioContext | null>(null);

    useEffect(() => {
        setMounted(true);
        const interval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
            const mins = Math.floor(elapsed / 60);
            const secs = elapsed % 60;
            setMetrics(prev => ({ ...prev, timeWasted: `${mins}m ${secs < 10 ? '0' : ''}${secs}s` }));
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isTyping]);

    const addLog = (msg: string) => {
        const time = new Date().toLocaleTimeString([], { hour12: false });
        setLogs(prev => [...prev, `[${time}] ${msg.toUpperCase()}`].slice(-10));
    };

    const handlePersonaChange = async (newPersona: 'grandma' | 'ramesh') => {
        setPersona(newPersona);
        if (room && room.state === 'connected') {
            await room.localParticipant.setMetadata(newPersona);
            addLog(`Persona Swapped: ${newPersona.toUpperCase()}`);
        }
    };

    // --- Voice Protocol Logic ---
    const toggleVoice = async () => {
        if (isVoiceConnected) {
            if (room) {
                await room.disconnect();
                setRoom(null);
            }
            setIsVoiceConnected(false);
            addLog("Voice Protocol Disconnected");
            return;
        }

        let lkRoom: LivekitClient.Room | null = null;
        try {
            addLog("Initializing Voice Protocol...");

            // Fetch dynamic token from backend
            addLog("Handshaking with Neural Server...");
            const tokenRes = await fetch('http://localhost:8000/token');
            if (!tokenRes.ok) throw new Error("Failed to fetch secure token");
            const { token, url } = await tokenRes.json();

            lkRoom = new LivekitClient.Room({ adaptiveStream: true });

            lkRoom.on(LivekitClient.RoomEvent.TrackSubscribed, (track) => {
                if (track.kind === 'audio') {
                    const el = track.attach();
                    document.body.appendChild(el);
                    el.play().then(() => {
                        addLog("Audio Output: ACTIVE");
                    }).catch(err => {
                        console.error("Autoplay thwarted:", err);
                        addLog("Audio Error: Click page to unmute");
                    });
                }
            });

            lkRoom.on(LivekitClient.RoomEvent.TranscriptionReceived, (transcriptions, participant) => {
                const role = participant?.identity === lkRoom!.localParticipant.identity ? 'scammer' : 'agent';

                transcriptions.forEach(t => {
                    const text = t.text.trim();
                    if (!text) return;

                    setMessages(prev => {
                        const existingIdx = prev.findIndex(m => m.id === t.id);
                        if (existingIdx !== -1) {
                            // Update existing message segment
                            const newMessages = [...prev];
                            newMessages[existingIdx] = {
                                ...newMessages[existingIdx],
                                text: text
                            };
                            return newMessages;
                        } else {
                            // NEW segment. Check if we should merge with last bubble
                            const last = prev[prev.length - 1];
                            if (last && last.role === role) {
                                const newMessages = [...prev];
                                newMessages[newMessages.length - 1] = {
                                    ...last,
                                    text: last.text + " " + text,
                                    id: t.id // Update ID to current so subsequent updates to THIS sentence hit here
                                };
                                return newMessages;
                            }
                            // New message segment (new role or first message)
                            return [...prev, {
                                id: t.id,
                                role,
                                text: text,
                                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                                source: 'voice'
                            }];
                        }
                    });

                    // Extract parameters passively (Scammer only)
                    if (role === 'scammer') {
                        // UPI ID
                        const upiRegex = /[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}/g;
                        const upis = text.match(upiRegex);
                        if (upis) {
                            setIntel(prev => ({
                                ...prev,
                                upiIds: Array.from(new Set([...prev.upiIds, ...upis]))
                            }));
                            addLog(`Neural Detected: UPI ID [${upis[0]}]`);
                        }

                        // Phone
                        const phoneRegex = /(\+?\d{1,4}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/g;
                        const phones = text.match(phoneRegex);
                        if (phones) {
                            setIntel(prev => ({
                                ...prev,
                                phoneNumbers: Array.from(new Set([...prev.phoneNumbers, ...phones]))
                            }));
                            addLog(`Neural Detected: PHONE [${phones[0]}]`);
                        }

                        // Location
                        const locationKeywords = /\b(Mumbai|Delhi|Bangalore|Chennai|Kolkata|London|New York|Dubai|Hyderabad|Pune|Ahmedabad|India)\b/gi;
                        const locations = text.match(locationKeywords);
                        if (locations) {
                            setIntel(prev => ({
                                ...prev,
                                location: Array.from(new Set([...prev.location, ...locations]))
                            }));
                            addLog(`Neural Detected: LOCATION [${locations[0]}]`);
                        }

                        // Name
                        const nameRegex = /my name is ([a-zA-Z\s]{1,30})/i;
                        const nameMatch = text.match(nameRegex);
                        if (nameMatch && nameMatch[1]) {
                            const name = nameMatch[1].trim();
                            setIntel(prev => ({
                                ...prev,
                                scammerName: Array.from(new Set([...prev.scammerName, name]))
                            }));
                            addLog(`Neural Detected: NAME [${name}]`);
                        }

                        // Update Metrics
                        setMetrics(prev => {
                            const newMoney = prev.moneySaved + Math.floor(Math.random() * 500) + 100;
                            return {
                                ...prev,
                                threatLevel: Math.min(prev.threatLevel + 2, 100),
                                fatigue: Math.min(prev.fatigue + 1, 100),
                                moneySaved: newMoney,
                                moneyHistory: [...prev.moneyHistory, newMoney].slice(-20)
                            };
                        });
                    }
                });
            });

            lkRoom.on(LivekitClient.RoomEvent.ActiveSpeakersChanged, (speakers) => {
                const agent = lkRoom!.remoteParticipants.values().next().value;
                const user = lkRoom!.localParticipant;

                setIsAgentSpeaking(speakers.some(s => s.identity === agent?.identity));
                setIsUserSpeaking(speakers.some(s => s.identity === user.identity));
            });

            lkRoom.on(LivekitClient.RoomEvent.Disconnected, () => {
                setIsVoiceConnected(false);
                setIsAgentSpeaking(false);
                setIsUserSpeaking(false);
                setRoom(null);
                addLog("Neural Link Terminated");
            });

            await lkRoom.connect(url, token);

            // Set metadata IMMEDIATELY to help agent identify persona
            await lkRoom.localParticipant.setMetadata(persona);
            addLog(`Identity Synced: ${persona.toUpperCase()}`);

            await lkRoom.localParticipant.setMicrophoneEnabled(true);
            addLog("Microphone Uplink: ENABLED");

            lkRoom.on(LivekitClient.RoomEvent.LocalTrackPublished, (pub) => {
                if (pub.kind === 'audio') {
                    addLog("MIC STREAM PUBLISHED TO CLOUD");
                }
            });

            lkRoom.on(LivekitClient.RoomEvent.ParticipantConnected, (p) => {
                addLog(`Node Discovery: ${p.identity} joined`);
            });

            setRoom(lkRoom);
            setIsVoiceConnected(true);
            addLog("NEURAL LINK: ESTABLISHED");

            // Initial speaker check
            const agent = lkRoom.remoteParticipants.values().next().value;
            setIsAgentSpeaking(agent?.isSpeaking || false);
            setIsUserSpeaking(lkRoom.localParticipant.isSpeaking);

        } catch (err: any) {
            console.error("Voice Error:", err);
            addLog(`Voice Error: ${err.message}`);

            // CRITICAL: If mic fails, we MUST disconnect to avoid zombie state
            if (lkRoom?.state === 'connected') {
                await lkRoom.disconnect();
                setRoom(null);
                setIsVoiceConnected(false);
            }

            if (window.location.protocol === 'http:' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
                alert("MICROPHONE BLOCKED: Browsers block microphone access on insecure (HTTP) connections over LAN/WiFi.\n\nPlease fallback to 'localhost' or setup HTTPS.");
                addLog("ERROR: INSECURE ORIGIN DETECTED");
            } else if (err.message.includes("Permission denied")) {
                alert("MICROPHONE BLOCKED: Please allow microphone access in your browser settings.");
            }
        }
    };

    const handleSendMessage = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (!inputValue.trim()) return;

        const userMsg: Message = {
            role: 'scammer',
            text: inputValue,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            source: 'text'
        };

        setMessages(prev => [...prev, userMsg]);
        setInputValue("");
        setIsTyping(true);
        addLog(`Intercepted: ${userMsg.text}`);

        try {
            const startTime = Date.now();
            const response = await fetch('http://localhost:8000/webhook', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-API-Key': '12345' },
                body: JSON.stringify({
                    sessionId: "console-session",
                    message: { text: userMsg.text, sender: 'scammer' },
                    conversationHistory: messages.map(m => ({ text: m.text, sender: m.role })),
                    metadata: { persona: persona }
                })
            });

            const data = await response.json();
            const latency = Date.now() - startTime;

            if (data.status === 'success') {
                const agentMsg: Message = {
                    role: 'agent',
                    text: data.reply,
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    source: 'text'
                };
                setMessages(prev => [...prev, agentMsg]);

                // Update Intel
                setIntel(prev => {
                    const newIntel = { ...prev };
                    Object.keys(data.intelligence).forEach(key => {
                        const typedKey = key as keyof Intelligence;
                        if (data.intelligence[key]) {
                            newIntel[typedKey] = Array.from(new Set([...(prev[typedKey] || []), ...data.intelligence[key]]));
                        }
                    });
                    return newIntel;
                });

                // Update Metrics
                setMetrics(prev => ({
                    ...prev,
                    threatLevel: (data.metrics?.confidence || 0) * 100,
                    latencyHistory: [...prev.latencyHistory, latency].slice(-10),
                    fatigue: Math.min(prev.fatigue + 10, 100),
                    moneySaved: prev.moneySaved + (data.intelligence.upiIds?.length ? 500 : 0)
                }));

                addLog(`AI RESPONSE :: LATENCY ${latency}ms`);
            }
        } catch (err) {
            addLog("ERROR :: BACKEND UNREACHABLE");
        } finally {
            setIsTyping(false);
        }
    };

    const resetSession = () => {
        setMessages([]);
        setIntel({ scammerName: [], bankAccounts: [], upiIds: [], phishingLinks: [], phoneNumbers: [], location: [], jobTitle: [] });
        setMetrics({ threatLevel: 0, fatigue: 0, timeWasted: "0m 00s", moneySaved: 0, moneyHistory: [0], latencyHistory: [] });
        startTimeRef.current = Date.now();
        addLog("PROTOCOL RESET :: SESSION PURGED");
    };

    if (!mounted) return null;

    return (
        <main className="w-full min-h-screen bg-[#F8FAFC] p-6 lg:p-12 selection:bg-indigo-500 selection:text-white flex flex-col gap-8">

            {/* BACKGROUND DECOR */}
            <div className="fixed inset-0 pointer-events-none -z-10 bg-grid-[#e2e8f0]/30 [mask-image:radial-gradient(white,transparent_85%)]"></div>
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-100/40 blur-[120px] rounded-full -z-10"></div>
            <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-purple-100/40 blur-[120px] rounded-full -z-10"></div>

            {/* HEADER ROW */}
            <header className="flex flex-col lg:flex-row justify-between items-center gap-8 shrink-0">
                <div className="flex items-center gap-6">
                    <Link href="/" className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center text-slate-900 shadow-xl hover:scale-110 transition-transform border border-slate-100">
                        <ChevronLeft size={24} />
                    </Link>
                    <div>
                        <h1 className="text-2xl font-black text-slate-800 tracking-tighter uppercase mb-1 flex items-center gap-3">
                            Vigilante <span className="text-indigo-600 bg-indigo-50 px-3 py-1 rounded-lg text-xs">PROTOCOL v2.5</span>
                        </h1>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Live Uplink</span>
                            </div>
                            <div className="text-[10px] font-black text-slate-300 uppercase tracking-widest border-l border-slate-200 pl-4">
                                Node: IND-MUM-01
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-6">
                    <div className="flex gap-2">
                        <PersonaCard
                            name="Mrs. Sharma" role="Honey-Pot" active={persona === 'grandma'} onClick={() => handlePersonaChange('grandma')}
                            avatar="https://i.pravatar.cc/100?u=grandma"
                        />
                        <PersonaCard
                            name="Ramesh Kumar" role="Skeptical" active={persona === 'ramesh'} onClick={() => handlePersonaChange('ramesh')}
                            avatar="https://i.pravatar.cc/100?u=ramesh"
                        />
                    </div>
                    <button
                        onClick={toggleVoice}
                        className={`flex flex-col items-center justify-center w-24 h-24 rounded-[2rem] border-2 transition-all duration-500 ${isVoiceConnected
                            ? isAgentSpeaking
                                ? 'bg-rose-500 border-rose-400 text-white shadow-xl shadow-rose-500/40 scale-105'
                                : isUserSpeaking
                                    ? 'bg-indigo-500 border-indigo-400 text-white shadow-xl shadow-indigo-500/40 scale-105'
                                    : 'bg-emerald-500 border-emerald-400 text-white shadow-xl shadow-emerald-500/20'
                            : 'bg-white border-slate-100 text-slate-400 hover:bg-slate-50'
                            }`}
                    >
                        <div className="relative">
                            {isVoiceConnected && (isAgentSpeaking || isUserSpeaking) && (
                                <motion.div
                                    initial={{ scale: 0.8, opacity: 0 }}
                                    animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }}
                                    transition={{ repeat: Infinity, duration: 1.5 }}
                                    className={`absolute inset-0 rounded-full blur-md -z-10 ${isAgentSpeaking ? 'bg-rose-400' : 'bg-indigo-400'}`}
                                />
                            )}
                            {isVoiceConnected ? <PhoneOff size={24} className="mb-2" /> : <Phone size={24} className="mb-2" />}
                        </div>
                        <span className="text-[8px] font-black uppercase tracking-tighter">
                            {isVoiceConnected
                                ? isAgentSpeaking ? "Agent Speaking" : isUserSpeaking ? "User Speaking" : "Sync Active"
                                : "Voice Sync"
                            }
                        </span>
                    </button>
                </div>
            </header>

            {/* MAIN LAYOUT GRID */}
            <div className="flex-1 grid grid-cols-12 gap-8 min-h-0">

                {/* LEFT: METRICS COLUMN */}
                <div className="col-span-12 lg:col-span-3 flex flex-col gap-6">
                    <CircularGauge value={metrics.threatLevel} label="Threat Level" active={isAgentSpeaking || isUserSpeaking} />
                    <FatigueThermometer value={metrics.fatigue} active={isAgentSpeaking} />
                    <MoneyGraph data={metrics.moneyHistory} current={metrics.moneySaved} />
                </div>

                {/* CENTER: CHAT INTERFACE */}
                <div className="col-span-12 lg:col-span-6 flex flex-col bg-white/50 backdrop-blur-xl rounded-[3rem] border border-white shadow-2xl relative overflow-hidden h-[600px] lg:h-[92vh]">
                    <div className="p-8 border-b border-slate-100 flex justify-between items-center bg-white/30">
                        <div className="flex items-center gap-3">
                            <Radio size={18} className="text-indigo-600 animate-pulse" />
                            <h3 className="text-sm font-black text-slate-800 uppercase tracking-widest">Active Interception</h3>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest bg-slate-100 px-4 py-2 rounded-full">
                                Time: {metrics.timeWasted}
                            </div>
                            <button onClick={resetSession} className="p-3 bg-indigo-50 text-indigo-600 rounded-2xl hover:bg-indigo-100 transition-colors">
                                <RefreshCw size={16} />
                            </button>
                        </div>
                    </div>

                    <div className="flex-1 overflow-y-auto p-10 space-y-6 scrollbar-thin scrollbar-thumb-indigo-200 scrollbar-track-transparent">
                        <AnimatePresence initial={false}>
                            {messages.map((m, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`flex ${m.role === 'agent' ? 'justify-start' : 'justify-end'}`}
                                >
                                    <div className={`max-w-[85%] p-6 rounded-[2rem] shadow-sm flex flex-col gap-2 ${m.role === 'agent'
                                        ? 'bg-indigo-600 text-white rounded-bl-none shadow-indigo-600/10'
                                        : 'bg-white text-slate-800 border border-slate-100 rounded-br-none shadow-slate-200/40'
                                        }`}>
                                        <div className="flex justify-between items-center gap-10">
                                            <span className={`text-[9px] font-black uppercase tracking-widest opacity-60 leading-none`}>
                                                {m.role === 'agent' ? 'VIGILANTE AI' : 'Intercept'}
                                            </span>
                                            <span className="text-[8px] font-bold opacity-40">{m.timestamp}</span>
                                        </div>
                                        <p className="font-bold leading-relaxed whitespace-pre-wrap break-words">{m.text}</p>
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                        {isTyping && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                                <div className="bg-indigo-600 text-white p-6 rounded-[2rem] rounded-bl-none shadow-sm flex gap-1">
                                    <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce"></div>
                                    <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce [animation-delay:0.2s]"></div>
                                    <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce [animation-delay:0.4s]"></div>
                                </div>
                            </motion.div>
                        )}
                        <div ref={chatEndRef} />
                    </div>

                    <form onSubmit={handleSendMessage} className="p-8 bg-white/50 border-t border-slate-100 flex gap-4">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Inject scam payload here..."
                            className="flex-1 px-8 py-5 bg-white border border-slate-100 rounded-[2rem] font-bold text-slate-700 focus:outline-none focus:border-indigo-600 shadow-inner"
                        />
                        <button type="submit" className="w-16 h-16 bg-slate-900 text-white rounded-[1.5rem] flex items-center justify-center hover:scale-105 transition-transform shadow-xl">
                            <Send size={20} />
                        </button>
                    </form>
                </div>

                {/* RIGHT COLUMN: INTEL & LOGS */}
                <div className="col-span-12 lg:col-span-3 flex flex-col gap-8">
                    <LatencySparkline data={metrics.latencyHistory} />

                    {/* INTEL CARDS */}
                    <div className="flex-1 bg-white border border-slate-100 rounded-[3rem] shadow-xl p-8 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-200 scrollbar-track-transparent flex flex-col">
                        <div className="flex items-center gap-3 mb-8">
                            <Brain size={18} className="text-purple-600" />
                            <h3 className="text-[10px] font-black text-slate-800 uppercase tracking-[0.2em]">Neural Extraction</h3>
                        </div>

                        <div className="flex-1 space-y-6">
                            {[
                                { label: 'UPI ID', val: intel.upiIds, color: 'text-emerald-500', bg: 'bg-emerald-50' },
                                { label: 'Target Name', val: intel.scammerName, color: 'text-indigo-500', bg: 'bg-indigo-50' },
                                { label: 'Location', val: intel.location, color: 'text-blue-500', bg: 'bg-blue-50' },
                                { label: 'Phone', val: intel.phoneNumbers, color: 'text-rose-500', bg: 'bg-rose-50' }
                            ].map((item, i) => (
                                <div key={i} className="flex flex-col gap-3">
                                    <div className="flex items-center justify-between px-1">
                                        <span className="text-[9px] font-black text-slate-300 uppercase tracking-widest">{item.label}</span>
                                        <span className={`text-[8px] font-black ${item.color} uppercase`}>{item.val.length > 0 ? 'Verified' : 'Searching'}</span>
                                    </div>
                                    <div className="flex flex-wrap gap-2">
                                        {item.val.length > 0 ? item.val.map((v, idx) => (
                                            <motion.span
                                                key={idx}
                                                initial={{ scale: 0.9, opacity: 0 }}
                                                animate={{ scale: 1, opacity: 1 }}
                                                className={`px-4 py-2 ${item.bg} ${item.color} rounded-xl text-[10px] font-black border border-white shadow-sm`}
                                            >
                                                {v}
                                            </motion.span>
                                        )) : (
                                            <div className="w-full h-1 bg-slate-50 rounded-full overflow-hidden">
                                                <motion.div className="h-full bg-slate-100 w-1/3" animate={{ x: ['0%', '200%'] }} transition={{ repeat: Infinity, duration: 1.5 }} />
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* MINIMAL TERMINAL */}
                    <div className="h-40 bg-white/40 backdrop-blur-xl border border-white rounded-[2.5rem] p-6 shadow-xl relative overflow-hidden flex flex-col">
                        <div className="flex items-center gap-3 mb-4">
                            <Terminal size={12} className="text-slate-400" />
                            <h4 className="text-[8px] font-black text-slate-400 uppercase tracking-[0.2em]">Protocol Debugger</h4>
                        </div>
                        <div className="flex-1 overflow-y-auto font-mono text-[9px] text-slate-600 space-y-1 scrollbar-thin scrollbar-thumb-slate-300 scrollbar-track-transparent">
                            {logs.map((log, i) => (
                                <div key={i}><span className="text-slate-300 mr-2">&gt;&gt;</span> {log}</div>
                            ))}
                        </div>
                    </div>

                </div>
            </div>
        </main>
    );
}

// Custom Icons for table items
function Briefcase(props: any) {
    return (
        <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" /><rect width="20" height="14" x="2" y="6" rx="2" />
        </svg>
    );
}
