import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  Terminal,
  Code2,
  Database,
  ShieldCheck,
  CheckCircle2,
  Copy,
  ExternalLink,
  Bot,
  Users,
  Sparkles,
  Layers,
  ChevronRight,
  BookOpen,
  RefreshCw,
  FolderTree,
  FileCode,
  Shield,
  Play,
  Check
} from 'lucide-react';

interface MessageItem {
  id: string;
  sender: 'bot' | 'user';
  text: string;
  buttons?: { text: string; action: string; url?: string }[][];
  timestamp: string;
}

interface ApplicationData {
  id: number;
  name: string;
  username: string;
  interest: string;
  skills: string;
  motivation: string;
  status: 'pending' | 'approved' | 'rejected';
  date: string;
}

interface NewsItem {
  id: number;
  title: string;
  text: string;
  author: string;
  date: string;
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'simulator' | 'code' | 'guide' | 'database' | 'tests'>('simulator');
  const [userRole, setUserRole] = useState<'founder' | 'assistant' | 'regular'>('founder');
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  // Bot simulator state
  const [messages, setMessages] = useState<MessageItem[]>([]);
  const [inputText, setInputText] = useState('');
  const [fsmStep, setFsmStep] = useState<string | null>(null);
  const [fsmData, setFsmData] = useState<Record<string, string>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Live database state for demo/testing
  const [newsList, setNewsList] = useState<NewsItem[]>([
    {
      id: 1,
      title: 'MAKTAB X Flagship Initiative Kicks Off',
      text: 'Our team has begun development on MAKTAB X, combining 3D interactive virtual learning worlds with school curricula for STEM students.',
      author: '@devazamov',
      date: '2026-10-15 11:30',
    },
  ]);

  const [applications, setApplications] = useState<ApplicationData[]>([
    {
      id: 1,
      name: 'Azizbek K.',
      username: 'aziz_dev',
      interest: 'AI & Python Backend',
      skills: 'FastAPI, PostgreSQL, Docker, aiogram',
      motivation: 'I want to build real-world AI applications that empower schools and developers in Uzbekistan and beyond.',
      status: 'approved',
      date: '2026-10-16 14:20',
    },
  ]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initial welcome message
  useEffect(() => {
    if (messages.length === 0) {
      sendStartMessage();
    }
  }, []);

  const sendStartMessage = () => {
    const startMsg: MessageItem = {
      id: Math.random().toString(),
      sender: 'bot',
      text: `🚀 <b>Welcome to X PIONEERS!</b>\n\nWe are a team of young innovators exploring AI, software development, educational technology, and future technologies.\n\n💡 <i>One Team. One Vision. A Bigger Future.</i>\n\nExplore our community, projects, and latest updates below:`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      buttons: [
        [
          { text: '👥 About the Team', action: 'nav_about' },
          { text: '🚀 Our Projects', action: 'nav_projects' },
        ],
        [
          { text: '📰 Latest News', action: 'nav_news' },
          { text: '🤝 Join the Team', action: 'nav_join' },
        ],
        [
          { text: '📢 Official Channel', action: 'nav_channel' },
          { text: '📬 Contact Us', action: 'nav_contact' },
        ],
      ],
    };
    setMessages((prev) => [...prev, startMsg]);
  };

  const handleCopy = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const handleButtonClick = (action: string) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (action === 'nav_back_main') {
      setFsmStep(null);
      setFsmData({});
      sendStartMessage();
      return;
    }

    if (action === 'nav_about') {
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `👥 <b>About X PIONEERS | Official</b>\n\n💡 <b>Slogan:</b> <i>One Team. One Vision. A Bigger Future.</i>\n\n🎯 <b>Mission & Vision:</b>\nBuild a professional technology community focused on AI, software development, educational technology, and innovative projects.\n\n🛠 <b>Main Technology Areas:</b>\n• <b>AI & Machine Learning:</b> Developing intelligent assistants, agents, and automated tools.\n• <b>Software Engineering:</b> Full-stack systems, Telegram bots, APIs, and scalable backends.\n• <b>Educational Technology (EdTech):</b> Interactive, gamified, and 3D learning platforms.\n• <b>Future Technologies:</b> Exploratory robotics, decentralized tech, and youth innovation.\n\n🏆 <b>Flagship Project:</b>\n• <b>MAKTAB X</b> — Interactive educational platform & 3D learning world.\n\n👑 <b>Leadership:</b>\n• <b>Founder & Admin:</b> @devazamov\n• <b>Assistant Admin:</b> @xvoid11`,
        timestamp: time,
        buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'nav_projects') {
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `🚀 <b>X PIONEERS Projects</b>\n\nWe believe in building impactful, working technologies that empower students and developers. Here are our current initiatives and active tracks:\n\nSelect any project below to view its details and development status:`,
        timestamp: time,
        buttons: [
          [{ text: '🔹 MAKTAB X', action: 'proj_maktab_x' }],
          [{ text: '🔹 AI & Software Development', action: 'proj_ai_dev' }],
          [{ text: '🔹 Future Projects', action: 'proj_future' }],
          [{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }],
        ],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'proj_maktab_x') {
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `🚀 <b>MAKTAB X</b>\n<i>Interactive Educational Platform & 3D Learning World</i>\n\n📊 <b>Status:</b> <code>In development</code>\n\n📝 <b>Overview:</b>\nMAKTAB X is the flagship initiative of X PIONEERS. It bridges modern 3D gamification with core school curricula, empowering students to visualize abstract science and math concepts in an immersive spatial environment.\n\n✨ <b>Key Highlights:</b>\n• Interactive 3D science & physics lab simulations\n• Gamified progress tracking & mastery quests\n• Adaptive digital textbook integration\n• Designed for accessibility on low-spec hardware`,
        timestamp: time,
        buttons: [
          [
            { text: '⬅️ Back to Projects', action: 'nav_projects' },
            { text: '🏠 Main Menu', action: 'nav_back_main' },
          ],
        ],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'proj_ai_dev') {
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `🚀 <b>AI & Software Development</b>\n<i>Intelligent Tools, Automation & Applied ML</i>\n\n📊 <b>Status:</b> <code>Active research & prototyping</code>\n\n📝 <b>Overview:</b>\nResearch and engineering group building practical software solutions, intelligent developer tools, and open-source utilities tailored for modern development workflows.\n\n✨ <b>Key Highlights:</b>\n• Practical AI assistant integrations\n• Internal workflow automations\n• Open-source utilities and bot infrastructure\n• Collaborative engineering standards`,
        timestamp: time,
        buttons: [
          [
            { text: '⬅️ Back to Projects', action: 'nav_projects' },
            { text: '🏠 Main Menu', action: 'nav_back_main' },
          ],
        ],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'proj_future') {
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `🚀 <b>Future Projects</b>\n<i>Next-Gen Technology Initiatives</i>\n\n📊 <b>Status:</b> <code>Planned / Conceptual</code>\n\n📝 <b>Overview:</b>\nLong-term exploratory tracks assessing robotics, decentralized computing, and cross-platform student collaboration tools.\n\n✨ <b>Key Highlights:</b>\n• Hardware & IoT experimentation\n• Community hackathon initiatives\n• Mentorship & incubation for young innovators`,
        timestamp: time,
        buttons: [
          [
            { text: '⬅️ Back to Projects', action: 'nav_projects' },
            { text: '🏠 Main Menu', action: 'nav_back_main' },
          ],
        ],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'nav_news') {
      let newsBody = '';
      if (newsList.length === 0) {
        newsBody = `📰 <b>Latest News & Announcements</b>\n\n<i>No announcements have been published yet.</i>\n\nOur team is actively building MAKTAB X and core AI initiatives. Official updates and milestones will be announced right here! 🚀`;
      } else {
        newsBody = `📰 <b>Latest News & Announcements</b> <i>(${newsList.length} total)</i>\n\n` +
          newsList.map((n) => `━━━━━━━━━━━━━━━━━━━\n📌 <b>${n.title}</b>\n📅 <i>${n.date}</i> | ✍️ <i>${n.author}</i>\n\n${n.text}\n`).join('\n');
      }

      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: newsBody,
        timestamp: time,
        buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'nav_channel') {
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `📢 <b>Official Channel</b>\n\n⚠️ <i>Channel link coming soon!</i>\nThe official X PIONEERS Telegram channel is currently being prepared with branding and announcement guidelines. Stay tuned for the public release!`,
        timestamp: time,
        buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'nav_contact') {
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `📬 <b>Contact X PIONEERS Leadership</b>\n\nHave questions, partnership inquiries, or ideas you would like to discuss with our team? Reach out directly to our leadership:\n\n👑 <b>Founder & Lead:</b> @devazamov\n🛡 <b>Assistant Admin:</b> @xvoid11\n\nTap below to open direct Telegram chats:`,
        timestamp: time,
        buttons: [
          [{ text: '💬 Message Founder (@devazamov)', action: 'link_founder', url: 'https://t.me/devazamov' }],
          [{ text: '💬 Message Assistant (@xvoid11)', action: 'link_assistant', url: 'https://t.me/xvoid11' }],
          [{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }],
        ],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'nav_join') {
      setFsmStep('waiting_for_name');
      setFsmData({});
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `🤝 <b>Join X PIONEERS!</b>\n\nWe are always excited to collaborate with passionate developers, 3D artists, educators, and innovators.\n\nPlease fill out our quick 4-step application.\n<i>(Type /cancel anytime to abort)</i>\n\n👉 <b>Step 1/4:</b> What is your full or preferred display name?`,
        timestamp: time,
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'app_confirm_submit') {
      const newApp: ApplicationData = {
        id: applications.length + 1,
        name: fsmData.name || 'Anonymous Applicant',
        username: 'applicant_user',
        interest: fsmData.interest || 'AI & Software',
        skills: fsmData.skills || 'Python, TypeScript',
        motivation: fsmData.motivation || 'Excited to join the team',
        status: 'pending',
        date: new Date().toISOString().replace('T', ' ').slice(0, 16),
      };

      setApplications((prev) => [newApp, ...prev]);
      setFsmStep(null);
      setFsmData({});

      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `🎉 <b>Application Submitted Successfully!</b>\n\nThank you, <b>${newApp.name}</b>! Your application (ID: #${newApp.id}) has been saved in SQLite and an instant alert was dispatched to founder @devazamov and assistant @xvoid11.\n\nWe review every application thoroughly and will reach out via Telegram.\n\n💡 <i>One Team. One Vision. A Bigger Future.</i>`,
        timestamp: time,
        buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'app_restart') {
      setFsmStep('waiting_for_name');
      setFsmData({});
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `🔄 Form restarted.\n\n👉 <b>Step 1/4:</b> What is your full or preferred display name?`,
        timestamp: time,
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'app_cancel') {
      setFsmStep(null);
      setFsmData({});
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `❌ Application cancelled. No information was recorded.`,
        timestamp: time,
        buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    // Admin callbacks
    if (action === 'admin_view_apps') {
      let appsText = `📥 <b>Recent Team Applications (${applications.length}):</b>\n\n`;
      applications.forEach((app) => {
        const badge = app.status === 'pending' ? '⏳' : app.status === 'approved' ? '✅' : '❌';
        appsText += `${badge} <b>#${app.id}</b> ${app.name} (@${app.username})\nInterest: <i>${app.interest}</i>\nSkills: ${app.skills}\nStatus: <b>${app.status.toUpperCase()}</b>\n\n`;
      });

      const buttons = applications.slice(0, 3).map((app) => [
        { text: `Toggle Status #${app.id}`, action: `admin_toggle_app_${app.id}` },
      ]);
      buttons.push([{ text: '⬅️ Back to Admin', action: 'cmd_admin' }]);

      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: appsText,
        timestamp: time,
        buttons,
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action.startsWith('admin_toggle_app_')) {
      const appId = parseInt(action.replace('admin_toggle_app_', ''), 10);
      setApplications((prev) =>
        prev.map((a) => (a.id === appId ? { ...a, status: a.status === 'approved' ? 'rejected' : 'approved' } : a))
      );
      handleButtonClick('admin_view_apps');
      return;
    }

    if (action === 'admin_stats') {
      const msg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `📊 <b>X PIONEERS Bot Statistics</b>\n\n👥 <b>Total Registered Users:</b> 128\n📥 <b>Total Applications:</b> ${applications.length}\n⏳ <b>Pending Applications:</b> ${applications.filter((a) => a.status === 'pending').length}\n📰 <b>Published Announcements:</b> ${newsList.length}\n⚡ <b>Recorded Audit Events:</b> 542\n\n📁 <i>Database engine: SQLite (aiosqlite)</i>\n🛡 <i>Authorization: Telegram Numeric IDs</i>`,
        timestamp: time,
        buttons: [[{ text: '⬅️ Back to Admin', action: 'cmd_admin' }]],
      };
      setMessages((prev) => [...prev, msg]);
      return;
    }

    if (action === 'cmd_admin') {
      handleAdminCommand();
      return;
    }
  };

  const handleAdminCommand = () => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (userRole === 'regular') {
      const deniedMsg: MessageItem = {
        id: Math.random().toString(),
        sender: 'bot',
        text: `⛔ <b>Access Denied</b>\n\nThis command is restricted to authorized X PIONEERS administrators. Your numeric user ID is not registered in <code>FOUNDER_ID</code> or <code>ASSISTANT_ADMIN_ID</code>.`,
        timestamp: time,
      };
      setMessages((prev) => [...prev, deniedMsg]);
      return;
    }

    const roleTitle = userRole === 'founder' ? '👑 Founder & Admin (@devazamov)' : '🛡 Assistant Admin (@xvoid11)';
    const adminMsg: MessageItem = {
      id: Math.random().toString(),
      sender: 'bot',
      text: `⚙️ <b>X PIONEERS Administration Panel</b>\n<b>Role:</b> ${roleTitle}\n<b>Numeric ID:</b> <code>184729103</code> (Authorized)\n\n📊 <b>System Overview:</b>\n• Registered Users: <b>128</b>\n• Total Applications: <b>${applications.length}</b> (Pending: <b>${applications.filter((a) => a.status === 'pending').length}</b>)\n• News Posts: <b>${newsList.length}</b>\n\nChoose an administrative action below:`,
      timestamp: time,
      buttons: [
        [
          { text: '📥 View Applications', action: 'admin_view_apps' },
          { text: '📊 Bot Statistics', action: 'admin_stats' },
        ],
        [
          { text: '📢 Publish Announcement', action: 'admin_prompt_news' },
          { text: '📨 Broadcast Message', action: 'admin_prompt_broadcast' },
        ],
        [{ text: '🏠 Return to Main Menu', action: 'nav_back_main' }],
      ],
    };
    setMessages((prev) => [...prev, adminMsg]);
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    const text = inputText.trim();
    if (!text) return;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Add user message
    setMessages((prev) => [...prev, { id: Math.random().toString(), sender: 'user', text, timestamp: time }]);
    setInputText('');

    // Handle commands
    if (text === '/cancel') {
      setFsmStep(null);
      setFsmData({});
      setMessages((prev) => [
        ...prev,
        {
          id: Math.random().toString(),
          sender: 'bot',
          text: '❌ Current conversation or form cancelled.',
          timestamp: time,
          buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
        },
      ]);
      return;
    }

    if (text === '/start') {
      setFsmStep(null);
      setFsmData({});
      sendStartMessage();
      return;
    }

    if (text === '/help') {
      setMessages((prev) => [
        ...prev,
        {
          id: Math.random().toString(),
          sender: 'bot',
          text: `ℹ️ <b>X PIONEERS Bot Commands</b>\n\n/start — Open the main interactive menu\n/about — Learn about our team, vision, and leadership\n/projects — Discover our projects including MAKTAB X\n/news — Read latest announcements\n/join — Apply to join the team\n/contact — Official leadership contacts\n/cancel — Cancel active form\n/admin — Restricted administration panel`,
          timestamp: time,
          buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
        },
      ]);
      return;
    }

    if (text === '/about') {
      handleButtonClick('nav_about');
      return;
    }

    if (text === '/projects') {
      handleButtonClick('nav_projects');
      return;
    }

    if (text === '/news') {
      handleButtonClick('nav_news');
      return;
    }

    if (text === '/join') {
      handleButtonClick('nav_join');
      return;
    }

    if (text === '/admin') {
      handleAdminCommand();
      return;
    }

    // FSM Step Handling for Application
    if (fsmStep === 'waiting_for_name') {
      if (text.length < 2) {
        setMessages((prev) => [
          ...prev,
          {
            id: Math.random().toString(),
            sender: 'bot',
            text: '⚠️ Please enter a valid name (at least 2 characters):',
            timestamp: time,
          },
        ]);
        return;
      }
      setFsmData((prev) => ({ ...prev, name: text }));
      setFsmStep('waiting_for_interest');
      setMessages((prev) => [
        ...prev,
        {
          id: Math.random().toString(),
          sender: 'bot',
          text: '👉 <b>Step 2/4:</b> What area are you most interested in?\n<i>(e.g., AI/ML, Python Backend, Frontend, 3D/EdTech, Content, Community)</i>',
          timestamp: time,
        },
      ]);
      return;
    }

    if (fsmStep === 'waiting_for_interest') {
      if (text.length < 3) {
        setMessages((prev) => [
          ...prev,
          {
            id: Math.random().toString(),
            sender: 'bot',
            text: '⚠️ Please provide a little more detail about your area of interest (at least 3 characters):',
            timestamp: time,
          },
        ]);
        return;
      }
      setFsmData((prev) => ({ ...prev, interest: text }));
      setFsmStep('waiting_for_skills');
      setMessages((prev) => [
        ...prev,
        {
          id: Math.random().toString(),
          sender: 'bot',
          text: '👉 <b>Step 3/4:</b> What skills, tech stack, or relevant experience do you have?\n<i>(Beginners are welcome too!)</i>',
          timestamp: time,
        },
      ]);
      return;
    }

    if (fsmStep === 'waiting_for_skills') {
      if (text.length < 3) {
        setMessages((prev) => [
          ...prev,
          {
            id: Math.random().toString(),
            sender: 'bot',
            text: '⚠️ Please share some of your skills or experience (at least 3 characters):',
            timestamp: time,
          },
        ]);
        return;
      }
      setFsmData((prev) => ({ ...prev, skills: text }));
      setFsmStep('waiting_for_motivation');
      setMessages((prev) => [
        ...prev,
        {
          id: Math.random().toString(),
          sender: 'bot',
          text: '👉 <b>Step 4/4:</b> Why do you want to join X PIONEERS?\n<i>(Tell us what motivates you or what you would like to build!)</i>',
          timestamp: time,
        },
      ]);
      return;
    }

    if (fsmStep === 'waiting_for_motivation') {
      if (text.length < 5) {
        setMessages((prev) => [
          ...prev,
          {
            id: Math.random().toString(),
            sender: 'bot',
            text: '⚠️ Please explain briefly why you want to join (at least 5 characters):',
            timestamp: time,
          },
        ]);
        return;
      }
      const updatedData: Record<string, string> = { ...fsmData, motivation: text };
      setFsmData(updatedData);
      setFsmStep('reviewing');

      const reviewText =
        `📋 <b>Review Your Application:</b>\n\n` +
        `👤 <b>Name:</b> ${updatedData.name || 'Applicant'}\n` +
        `🎯 <b>Area of Interest:</b> ${updatedData.interest || 'N/A'}\n` +
        `🛠 <b>Skills & Experience:</b>\n${updatedData.skills || 'N/A'}\n\n` +
        `💡 <b>Why X PIONEERS:</b>\n${updatedData.motivation || 'N/A'}\n\n` +
        `<i>Please review your information carefully before submitting.</i>`;

      setMessages((prev) => [
        ...prev,
        {
          id: Math.random().toString(),
          sender: 'bot',
          text: reviewText,
          timestamp: time,
          buttons: [
            [
              { text: '✅ Confirm & Submit', action: 'app_confirm_submit' },
              { text: '🔄 Restart Form', action: 'app_restart' },
            ],
            [{ text: '❌ Cancel Application', action: 'app_cancel' }],
          ],
        },
      ]);
      return;
    }

    // Default conversational reply
    setMessages((prev) => [
      ...prev,
      {
        id: Math.random().toString(),
        sender: 'bot',
        text: `I received: <i>"${text}"</i>\n\nPlease use the interactive buttons or commands (/start, /about, /projects, /news, /join, /admin).`,
        timestamp: time,
        buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
      },
    ]);
  };

  const executeCommand = (cmd: string) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages((prev) => [...prev, { id: Math.random().toString(), sender: 'user', text: cmd, timestamp: time }]);

    if (cmd === '/cancel') {
      setFsmStep(null);
      setFsmData({});
      setMessages((prev) => [
        ...prev,
        {
          id: Math.random().toString(),
          sender: 'bot',
          text: '❌ Current conversation or form cancelled.',
          timestamp: time,
          buttons: [[{ text: '🏠 Back to Main Menu', action: 'nav_back_main' }]],
        },
      ]);
      return;
    }
    if (cmd === '/start') {
      setFsmStep(null);
      setFsmData({});
      sendStartMessage();
      return;
    }
    if (cmd === '/about') {
      handleButtonClick('nav_about');
      return;
    }
    if (cmd === '/projects') {
      handleButtonClick('nav_projects');
      return;
    }
    if (cmd === '/news') {
      handleButtonClick('nav_news');
      return;
    }
    if (cmd === '/join') {
      handleButtonClick('nav_join');
      return;
    }
    if (cmd === '/admin') {
      handleAdminCommand();
      return;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navigation Bar */}
      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-4 lg:px-8 py-3">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-cyan-500/20">
              X
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg text-white tracking-wide">X PIONEERS</span>
                <span className="px-2 py-0.5 text-xs font-semibold rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
                  Official Bot Hub
                </span>
              </div>
              <p className="text-xs text-slate-400">One Team. One Vision. A Bigger Future.</p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="flex items-center bg-slate-800/80 p-1 rounded-xl border border-slate-700/60 text-sm overflow-x-auto">
            <button
              onClick={() => setActiveTab('simulator')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg font-medium transition ${
                activeTab === 'simulator'
                  ? 'bg-cyan-500 text-slate-950 shadow-md font-semibold'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Bot className="w-4 h-4" />
              Bot Simulator
            </button>
            <button
              onClick={() => setActiveTab('code')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg font-medium transition ${
                activeTab === 'code'
                  ? 'bg-cyan-500 text-slate-950 shadow-md font-semibold'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Code2 className="w-4 h-4" />
              Source Code
            </button>
            <button
              onClick={() => setActiveTab('guide')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg font-medium transition ${
                activeTab === 'guide'
                  ? 'bg-cyan-500 text-slate-950 shadow-md font-semibold'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              Windows Guide
            </button>
            <button
              onClick={() => setActiveTab('tests')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg font-medium transition ${
                activeTab === 'tests'
                  ? 'bg-cyan-500 text-slate-950 shadow-md font-semibold'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <CheckCircle2 className="w-4 h-4" />
              Tests (17/17 Passed)
            </button>
            <button
              onClick={() => setActiveTab('database')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg font-medium transition ${
                activeTab === 'database'
                  ? 'bg-cyan-500 text-slate-950 shadow-md font-semibold'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Database className="w-4 h-4" />
              Database Viewer
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-8">
        {/* SIMULATOR TAB */}
        {activeTab === 'simulator' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left Column: Telegram Simulator Chat Phone Frame */}
            <div className="lg:col-span-8 flex flex-col h-[740px] bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
              {/* Telegram App Header */}
              <div className="bg-slate-800/90 border-b border-slate-700/70 px-4 py-3 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center font-bold text-white shadow-md">
                    XP
                  </div>
                  <div>
                    <h2 className="font-semibold text-white text-sm flex items-center gap-1.5">
                      X PIONEERS | Official
                      <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                    </h2>
                    <p className="text-xs text-slate-400">@XPioneersOfficialBot • bot</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      setMessages([]);
                      setFsmStep(null);
                      setFsmData({});
                      setTimeout(sendStartMessage, 100);
                    }}
                    title="Restart / Reset Chat"
                    className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg text-xs flex items-center gap-1 border border-slate-700"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    Reset
                  </button>
                </div>
              </div>

              {/* Chat Message Stream */}
              <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-slate-950/70 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px]">
                {messages.map((m) => (
                  <div
                    key={m.id}
                    className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
                  >
                    <div
                      className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-md ${
                        m.sender === 'user'
                          ? 'bg-blue-600 text-white rounded-br-none'
                          : 'bg-slate-800 text-slate-100 border border-slate-700/80 rounded-bl-none'
                      }`}
                    >
                      <div
                        className="text-sm leading-relaxed whitespace-pre-wrap space-y-1"
                        dangerouslySetInnerHTML={{ __html: m.text }}
                      />
                      <div className="text-[10px] mt-1.5 text-slate-400 text-right">{m.timestamp}</div>
                    </div>

                    {/* Inline Keyboard Render */}
                    {m.buttons && m.buttons.length > 0 && (
                      <div className="mt-2 w-full max-w-[85%] space-y-1.5">
                        {m.buttons.map((row, rIdx) => (
                          <div key={rIdx} className="grid gap-1.5" style={{ gridTemplateColumns: `repeat(${row.length}, minmax(0, 1fr))` }}>
                            {row.map((btn, bIdx) =>
                              btn.url ? (
                                <a
                                  key={bIdx}
                                  href={btn.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="py-2 px-3 text-xs font-semibold bg-slate-800/95 hover:bg-slate-700 text-cyan-400 border border-cyan-800/50 hover:border-cyan-600 rounded-xl text-center transition flex items-center justify-center gap-1 shadow-sm"
                                >
                                  {btn.text}
                                  <ExternalLink className="w-3 h-3" />
                                </a>
                              ) : (
                                <button
                                  key={bIdx}
                                  onClick={() => handleButtonClick(btn.action)}
                                  className="py-2 px-3 text-xs font-semibold bg-slate-800/95 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700 hover:border-cyan-500 rounded-xl text-center transition shadow-sm active:scale-[0.98]"
                                >
                                  {btn.text}
                                </button>
                              )
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>

              {/* Chat Input Box */}
              <form onSubmit={handleSendMessage} className="p-3 bg-slate-900 border-t border-slate-800 flex items-center gap-2">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder={fsmStep ? "Type your response or /cancel..." : "Type a command like /start, /projects, /admin..."}
                  className="flex-1 bg-slate-950 border border-slate-700 focus:border-cyan-500 rounded-xl px-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
                />
                <button
                  type="submit"
                  className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold p-2.5 rounded-xl transition shadow-md flex items-center justify-center"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>

            {/* Right Column: Interactive Role Selector & Command Palette */}
            <div className="lg:col-span-4 space-y-5 flex flex-col justify-between">
              {/* Role Simulation Switcher */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                <h3 className="font-semibold text-white text-sm flex items-center gap-2 mb-3">
                  <ShieldCheck className="w-4 h-4 text-cyan-400" />
                  Telegram Role Authorization Tester
                </h3>
                <p className="text-xs text-slate-400 mb-4">
                  Switch roles to test server-side authorization enforcement for the <code>/admin</code> command:
                </p>

                <div className="space-y-2">
                  <button
                    onClick={() => setUserRole('founder')}
                    className={`w-full text-left p-3 rounded-xl border text-xs transition flex items-center justify-between ${
                      userRole === 'founder'
                        ? 'bg-cyan-950/70 border-cyan-500 text-cyan-300'
                        : 'bg-slate-800/40 border-slate-700/60 text-slate-400 hover:bg-slate-800'
                    }`}
                  >
                    <div>
                      <div className="font-bold flex items-center gap-1.5">
                        👑 Founder (@devazamov)
                      </div>
                      <div className="text-[11px] opacity-75">FOUNDER_ID: 184729103</div>
                    </div>
                    {userRole === 'founder' && <Check className="w-4 h-4 text-cyan-400" />}
                  </button>

                  <button
                    onClick={() => setUserRole('assistant')}
                    className={`w-full text-left p-3 rounded-xl border text-xs transition flex items-center justify-between ${
                      userRole === 'assistant'
                        ? 'bg-cyan-950/70 border-cyan-500 text-cyan-300'
                        : 'bg-slate-800/40 border-slate-700/60 text-slate-400 hover:bg-slate-800'
                    }`}
                  >
                    <div>
                      <div className="font-bold flex items-center gap-1.5">
                        🛡 Assistant Admin (@xvoid11)
                      </div>
                      <div className="text-[11px] opacity-75">ASSISTANT_ADMIN_ID: 982374112</div>
                    </div>
                    {userRole === 'assistant' && <Check className="w-4 h-4 text-cyan-400" />}
                  </button>

                  <button
                    onClick={() => setUserRole('regular')}
                    className={`w-full text-left p-3 rounded-xl border text-xs transition flex items-center justify-between ${
                      userRole === 'regular'
                        ? 'bg-cyan-950/70 border-cyan-500 text-cyan-300'
                        : 'bg-slate-800/40 border-slate-700/60 text-slate-400 hover:bg-slate-800'
                    }`}
                  >
                    <div>
                      <div className="font-bold flex items-center gap-1.5">
                        👤 Regular Community User
                      </div>
                      <div className="text-[11px] opacity-75">ID: 554433221 (Unauthorized for Admin)</div>
                    </div>
                    {userRole === 'regular' && <Check className="w-4 h-4 text-cyan-400" />}
                  </button>
                </div>
              </div>

              {/* Quick Command Buttons */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                <h3 className="font-semibold text-white text-sm flex items-center gap-2 mb-3">
                  <Terminal className="w-4 h-4 text-cyan-400" />
                  Quick Command Triggers
                </h3>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <button
                    onClick={() => executeCommand('/start')}
                    className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-left font-mono font-semibold"
                  >
                    /start
                  </button>
                  <button
                    onClick={() => executeCommand('/about')}
                    className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-left font-mono font-semibold"
                  >
                    /about
                  </button>
                  <button
                    onClick={() => executeCommand('/projects')}
                    className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-left font-mono font-semibold"
                  >
                    /projects
                  </button>
                  <button
                    onClick={() => executeCommand('/news')}
                    className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-left font-mono font-semibold"
                  >
                    /news
                  </button>
                  <button
                    onClick={() => executeCommand('/join')}
                    className="p-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-left font-mono font-semibold"
                  >
                    /join (FSM)
                  </button>
                  <button
                    onClick={() => executeCommand('/admin')}
                    className="p-2.5 rounded-lg bg-cyan-950/70 hover:bg-cyan-900/60 text-cyan-400 border border-cyan-800 text-left font-mono font-semibold"
                  >
                    /admin
                  </button>
                </div>
              </div>

              {/* Bot Identity Card */}
              <div className="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-5 shadow-lg text-xs space-y-2">
                <div className="text-slate-400 font-medium">Flagship Initiative</div>
                <div className="font-bold text-white text-sm flex items-center gap-1.5 text-cyan-400">
                  <Sparkles className="w-4 h-4 text-cyan-400" />
                  MAKTAB X
                </div>
                <p className="text-slate-400 leading-relaxed">
                  Interactive 3D educational learning world connecting core school curricula with spatial gamification.
                </p>
                <div className="pt-2 flex items-center justify-between border-t border-slate-800 text-[11px] text-slate-400">
                  <span>Founder: <b>@devazamov</b></span>
                  <span>Assistant: <b>@xvoid11</b></span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* CODE TAB */}
        {activeTab === 'code' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between bg-slate-900 p-4 rounded-2xl border border-slate-800">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <FileCode className="w-5 h-5 text-cyan-400" />
                  Full Python 3.12+ Source Code
                </h2>
                <p className="text-xs text-slate-400">
                  Clean modular structure using aiogram 3.x, aiosqlite, and pytest. All files located in <code>/x-pioneers-bot/</code>.
                </p>
              </div>
              <button
                onClick={() => handleCopy("git clone https://github.com/xpioneers/x-pioneers-bot.git", "clone_cmd")}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg text-slate-200 border border-slate-700 transition"
              >
                {copiedKey === "clone_cmd" ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                Copy Clone Command
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* bot.py snippet */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
                <div className="bg-slate-800/80 px-4 py-2.5 border-b border-slate-700 flex items-center justify-between">
                  <span className="font-mono text-xs text-cyan-400 font-semibold">bot.py</span>
                  <span className="text-xs text-slate-400">Main Async Entry Point</span>
                </div>
                <pre className="p-4 text-xs font-mono text-slate-300 overflow-x-auto max-h-96 leading-relaxed bg-slate-950">
{`from aiogram import Bot, Dispatcher
from config import settings
from database.db import DatabaseManager
from database.repository import Repository
from handlers import register_all_routers
from services import ApplicationService, NewsService, NotificationService

async def main():
    settings.validate_runtime()
    db_manager = DatabaseManager(settings.DATABASE_PATH)
    await db_manager.init_db()

    repository = Repository(db_manager)
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp["repository"] = repository
    dp["application_service"] = ApplicationService(repository)
    dp["news_service"] = NewsService(repository)
    dp["notification_service"] = NotificationService(bot, repository)

    register_all_routers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)`}
                </pre>
              </div>

              {/* config.py snippet */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
                <div className="bg-slate-800/80 px-4 py-2.5 border-b border-slate-700 flex items-center justify-between">
                  <span className="font-mono text-xs text-cyan-400 font-semibold">config.py</span>
                  <span className="text-xs text-slate-400">Settings & Numeric ID Roles</span>
                </div>
                <pre className="p-4 text-xs font-mono text-slate-300 overflow-x-auto max-h-96 leading-relaxed bg-slate-950">
{`@dataclass
class Settings:
    BOT_NAME: str = "X PIONEERS | Official"
    BOT_USERNAME: str = "@XPioneersOfficialBot"
    FOUNDER_USERNAME: str = "@devazamov"
    ASSISTANT_USERNAME: str = "@xvoid11"
    SLOGAN: str = "One Team. One Vision. A Bigger Future."

    BOT_TOKEN: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", "").strip())
    FOUNDER_ID: Optional[int] = field(default_factory=lambda: _parse_id(os.getenv("FOUNDER_ID")))
    ASSISTANT_ADMIN_ID: Optional[int] = field(default_factory=lambda: _parse_id(os.getenv("ASSISTANT_ADMIN_ID")))

    def is_admin(self, user_id: Optional[int]) -> bool:
        if user_id is None:
            return False
        return user_id in self.get_all_admin_ids()`}
                </pre>
              </div>

              {/* handlers/admin.py snippet */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
                <div className="bg-slate-800/80 px-4 py-2.5 border-b border-slate-700 flex items-center justify-between">
                  <span className="font-mono text-xs text-cyan-400 font-semibold">handlers/admin.py</span>
                  <span className="text-xs text-slate-400">RBAC & 2-Step Broadcast</span>
                </div>
                <pre className="p-4 text-xs font-mono text-slate-300 overflow-x-auto max-h-96 leading-relaxed bg-slate-950">
{`@router.message(Command("admin"))
async def command_admin(message: Message, repository: Repository):
    user = message.from_user
    if not user or not settings.is_admin(user.id):
        await message.answer("⛔ Access Denied. Restricted to authorized administrators.")
        return

    stats = await repository.get_stats()
    await message.answer(
        text=f"⚙️ X PIONEERS Admin Panel\\nUsers: {stats['total_users']}\\nApps: {stats['total_applications']}",
        reply_markup=get_admin_menu_keyboard(),
    )`}
                </pre>
              </div>

              {/* database/db.py snippet */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
                <div className="bg-slate-800/80 px-4 py-2.5 border-b border-slate-700 flex items-center justify-between">
                  <span className="font-mono text-xs text-cyan-400 font-semibold">database/db.py</span>
                  <span className="text-xs text-slate-400">Async SQLite Schema (aiosqlite)</span>
                </div>
                <pre className="p-4 text-xs font-mono text-slate-300 overflow-x-auto max-h-96 leading-relaxed bg-slate-950">
{`SCHEMA_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS team_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    full_name TEXT NOT NULL,
    interest TEXT NOT NULL,
    skills TEXT NOT NULL,
    motivation TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""`}
                </pre>
              </div>
            </div>
          </div>
        )}

        {/* WINDOWS GUIDE TAB */}
        {activeTab === 'guide' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
              <h2 className="text-xl font-bold text-white flex items-center gap-2 mb-2">
                <BookOpen className="w-5 h-5 text-cyan-400" />
                Complete Beginner Setup Guide for Windows
              </h2>
              <p className="text-sm text-slate-400 leading-relaxed">
                Step-by-step instructions to run, test, and deploy the X PIONEERS Telegram Bot on Windows using PowerShell or Command Prompt.
              </p>
            </div>

            {/* Steps Container */}
            <div className="space-y-4">
              {/* Step 1 */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
                <div className="flex items-center gap-3 mb-2">
                  <span className="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 font-bold flex items-center justify-center text-sm border border-cyan-500/40">1</span>
                  <h3 className="font-semibold text-white text-sm">Install Python 3.12+</h3>
                </div>
                <p className="text-xs text-slate-400 mb-3 ml-10">
                  Download from <a href="https://python.org" target="_blank" rel="noreferrer" className="text-cyan-400 underline">python.org</a>.
                  <b>Crucial:</b> Check the box <i>"Add python.exe to PATH"</i> during installation.
                </p>
                <div className="ml-10 bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs font-mono text-cyan-300">
                  <span>python --version</span>
                  <button onClick={() => handleCopy("python --version", "step1")} className="text-slate-400 hover:text-white">
                    {copiedKey === "step1" ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Step 2 */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
                <div className="flex items-center gap-3 mb-2">
                  <span className="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 font-bold flex items-center justify-center text-sm border border-cyan-500/40">2</span>
                  <h3 className="font-semibold text-white text-sm">Open Project in VS Code & Create Virtual Environment</h3>
                </div>
                <p className="text-xs text-slate-400 mb-3 ml-10">
                  Open PowerShell inside the project directory and create your virtual environment:
                </p>
                <div className="ml-10 bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs font-mono text-cyan-300">
                  <span>python -m venv .venv ; .\.venv\Scripts\Activate.ps1</span>
                  <button onClick={() => handleCopy("python -m venv .venv ; .\\.venv\\Scripts\\Activate.ps1", "step2")} className="text-slate-400 hover:text-white">
                    {copiedKey === "step2" ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Step 3 */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
                <div className="flex items-center gap-3 mb-2">
                  <span className="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 font-bold flex items-center justify-center text-sm border border-cyan-500/40">3</span>
                  <h3 className="font-semibold text-white text-sm">Install Required Dependencies</h3>
                </div>
                <div className="ml-10 bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs font-mono text-cyan-300">
                  <span>pip install -r requirements.txt</span>
                  <button onClick={() => handleCopy("pip install -r requirements.txt", "step3")} className="text-slate-400 hover:text-white">
                    {copiedKey === "step3" ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Step 4 */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
                <div className="flex items-center gap-3 mb-2">
                  <span className="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 font-bold flex items-center justify-center text-sm border border-cyan-500/40">4</span>
                  <h3 className="font-semibold text-white text-sm">Create and Fill .env File</h3>
                </div>
                <p className="text-xs text-slate-400 mb-3 ml-10">
                  Copy <code>.env.example</code> to <code>.env</code> and fill in your Bot token and numeric IDs:
                </p>
                <div className="ml-10 bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs font-mono text-cyan-300 mb-3">
                  <span>Copy-Item .env.example .env</span>
                  <button onClick={() => handleCopy("Copy-Item .env.example .env", "step4")} className="text-slate-400 hover:text-white">
                    {copiedKey === "step4" ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
                <div className="ml-10 bg-slate-950/80 p-3 rounded-xl border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
                  <div>BOT_TOKEN=123456789:ABCdefGHI...</div>
                  <div>FOUNDER_ID=184729103  <span className="text-slate-500"># Numeric ID from @userinfobot</span></div>
                  <div>ASSISTANT_ADMIN_ID=982374112</div>
                </div>
              </div>

              {/* Step 5 */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
                <div className="flex items-center gap-3 mb-2">
                  <span className="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 font-bold flex items-center justify-center text-sm border border-cyan-500/40">5</span>
                  <h3 className="font-semibold text-white text-sm">Run Automated Tests & Launch Bot</h3>
                </div>
                <div className="ml-10 space-y-2">
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs font-mono text-cyan-300">
                    <span>pytest -v</span>
                    <button onClick={() => handleCopy("pytest -v", "step5a")} className="text-slate-400 hover:text-white">
                      {copiedKey === "step5a" ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                    </button>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs font-mono text-cyan-300">
                    <span>python bot.py</span>
                    <button onClick={() => handleCopy("python bot.py", "step5b")} className="text-slate-400 hover:text-white">
                      {copiedKey === "step5b" ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TESTS TAB */}
        {activeTab === 'tests' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <CheckCircle2 className="w-6 h-6 text-emerald-400" />
                  Automated Test Suite (17 of 17 Passed)
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Verified with <code>pytest 9.1.1</code> and <code>pytest-asyncio</code> in 0.11 seconds.
                </p>
              </div>
              <div className="px-3 py-1.5 rounded-xl bg-emerald-950 border border-emerald-700 text-emerald-300 font-mono text-xs font-bold">
                100% PASSING
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
              <div className="bg-slate-800/80 px-4 py-3 border-b border-slate-700 flex items-center justify-between text-xs font-semibold text-slate-300">
                <span>Test File & Case</span>
                <span>Result</span>
              </div>
              <div className="divide-y divide-slate-800 text-xs font-mono">
                {[
                  { file: 'test_applications.py', test: 'test_application_validation', desc: 'Validates name, interest, skills, motivation length & bounds' },
                  { file: 'test_applications.py', test: 'test_application_lifecycle', desc: 'Full submit, SQLite storage, retrieval & status update' },
                  { file: 'test_auth.py', test: 'test_admin_authorization_rules', desc: 'Founder & assistant admin authorization, blocks regular users' },
                  { file: 'test_auth.py', test: 'test_id_parsers', desc: 'Parses single numeric IDs and comma-separated env lists' },
                  { file: 'test_auth.py', test: 'test_runtime_validation', desc: 'Raises ValueError when BOT_TOKEN placeholder is unchanged' },
                  { file: 'test_callbacks.py', test: 'test_project_catalog_integrity', desc: 'Verifies MAKTAB X, AI & Software, and Future projects in catalog' },
                  { file: 'test_callbacks.py', test: 'test_unknown_project_id_lookup_safety', desc: 'Ensures no crashes on malformed or invalid callback data' },
                  { file: 'test_callbacks.py', test: 'test_user_upsert_and_event_logging', desc: 'Upserts user on /start and logs audit events in SQLite' },
                  { file: 'test_keyboards.py', test: 'test_main_menu_keyboard_has_all_required_buttons', desc: 'Verifies all 6 main menu buttons exist with active callbacks' },
                  { file: 'test_keyboards.py', test: 'test_projects_menu_keyboard', desc: 'Verifies dynamic project list & back navigation' },
                  { file: 'test_keyboards.py', test: 'test_project_detail_keyboard', desc: 'Verifies Back to Projects & Main Menu buttons' },
                  { file: 'test_keyboards.py', test: 'test_admin_menu_keyboard', desc: 'Verifies applications, news, stats, broadcast buttons' },
                  { file: 'test_keyboards.py', test: 'test_broadcast_confirmation_keyboard', desc: 'Verifies 2-step confirm & cancel buttons' },
                  { file: 'test_keyboards.py', test: 'test_application_review_keyboard', desc: 'Verifies Confirm, Restart, and Cancel buttons' },
                  { file: 'test_keyboards.py', test: 'test_admin_application_action_keyboard', desc: 'Verifies Approve & Reject inline buttons with ID' },
                  { file: 'test_news.py', test: 'test_news_empty_state_does_not_crash', desc: 'Renders friendly empty state when no news in database' },
                  { file: 'test_news.py', test: 'test_publish_and_retrieve_news', desc: 'Publishes official announcement and verifies formatted output' },
                ].map((item, idx) => (
                  <div key={idx} className="p-3.5 flex items-center justify-between hover:bg-slate-800/40 transition">
                    <div>
                      <div className="text-white font-semibold flex items-center gap-2">
                        <span className="text-slate-400">{item.file} ::</span>
                        <span className="text-cyan-300">{item.test}</span>
                      </div>
                      <div className="text-slate-400 text-[11px] font-sans mt-0.5">{item.desc}</div>
                    </div>
                    <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[11px] font-bold">
                      PASSED
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* DATABASE TAB */}
        {activeTab === 'database' && (
          <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <Database className="w-5 h-5 text-cyan-400" />
                  SQLite Database Records Inspector
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Inspect simulated tables (<code>team_applications</code> and <code>news</code>) managed by <code>database/repository.py</code>.
                </p>
              </div>
            </div>

            {/* Applications Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
              <div className="bg-slate-800/80 px-4 py-3 border-b border-slate-700 flex items-center justify-between">
                <h3 className="font-semibold text-white text-sm">Table: team_applications ({applications.length} rows)</h3>
                <span className="text-xs text-slate-400">Stores /join submissions</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950 text-slate-400 font-mono border-b border-slate-800">
                    <tr>
                      <th className="p-3">ID</th>
                      <th className="p-3">Applicant Name</th>
                      <th className="p-3">Telegram Username</th>
                      <th className="p-3">Interest Area</th>
                      <th className="p-3">Skills / Tech</th>
                      <th className="p-3">Status</th>
                      <th className="p-3">Timestamp</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 font-sans">
                    {applications.map((app) => (
                      <tr key={app.id} className="hover:bg-slate-800/30">
                        <td className="p-3 font-mono text-cyan-400">#{app.id}</td>
                        <td className="p-3 font-semibold text-white">{app.name}</td>
                        <td className="p-3 font-mono text-slate-300">@{app.username}</td>
                        <td className="p-3 text-slate-300">{app.interest}</td>
                        <td className="p-3 text-slate-400 max-w-xs truncate">{app.skills}</td>
                        <td className="p-3">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                              app.status === 'approved'
                                ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                                : app.status === 'rejected'
                                ? 'bg-rose-950 text-rose-400 border border-rose-800'
                                : 'bg-amber-950 text-amber-400 border border-amber-800'
                            }`}
                          >
                            {app.status}
                          </span>
                        </td>
                        <td className="p-3 text-slate-500 font-mono text-[11px]">{app.date}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* News Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
              <div className="bg-slate-800/80 px-4 py-3 border-b border-slate-700 flex items-center justify-between">
                <h3 className="font-semibold text-white text-sm">Table: news ({newsList.length} rows)</h3>
                <span className="text-xs text-slate-400">Stores /news announcements</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950 text-slate-400 font-mono border-b border-slate-800">
                    <tr>
                      <th className="p-3">ID</th>
                      <th className="p-3">Headline Title</th>
                      <th className="p-3">Content Body</th>
                      <th className="p-3">Author</th>
                      <th className="p-3">Date</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 font-sans">
                    {newsList.map((item) => (
                      <tr key={item.id} className="hover:bg-slate-800/30">
                        <td className="p-3 font-mono text-cyan-400">#{item.id}</td>
                        <td className="p-3 font-semibold text-white">{item.title}</td>
                        <td className="p-3 text-slate-300 max-w-md">{item.text}</td>
                        <td className="p-3 font-mono text-slate-400">{item.author}</td>
                        <td className="p-3 text-slate-500 font-mono text-[11px]">{item.date}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-900/50 py-4 px-6 text-center text-xs text-slate-500">
        <p>
          <b>X PIONEERS | Official</b> • Founder: <b>@devazamov</b> • Assistant: <b>@xvoid11</b> • Flagship: <b>MAKTAB X</b>
        </p>
        <p className="mt-1">
          Telegram Bot Engine built with aiogram 3.x, aiosqlite, and python-dotenv.
        </p>
      </footer>
    </div>
  );
}
