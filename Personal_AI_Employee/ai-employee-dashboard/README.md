# AI Employee Dashboard

A premium, enterprise-grade Next.js dashboard for your Personal AI Employee project. Built with modern technologies to provide a $50,000+ SaaS-quality experience.

## 🚀 Features

- **Premium Dark Theme**: Beautiful glassmorphism design with smooth animations
- **Real-time Data**: Connects to your AI_Employee_Vault for live updates
- **Interactive Components**: Charts, kanban boards, and activity feeds
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- **Performance Optimized**: Built with Next.js best practices

## 🛠️ Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom theme
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Icons**: Lucide React
- **State Management**: React Hooks
- **Data Fetching**: Next.js API Routes

## 📦 Installation

1. Clone or copy this dashboard into your project:

```bash
cd your-project-directory
# Copy the ai-employee-dashboard folder to your project
```

2. Install dependencies:

```bash
cd ai-employee-dashboard
npm install
```

3. Set up environment variables:

```bash
cp .env.example .env.local
```

Edit `.env.local` and update the `VAULT_PATH` to point to your AI_Employee_Vault:

```env
VAULT_PATH=../AI_Employee_Vault
NEXT_PUBLIC_APP_NAME=AI Employee Dashboard
NEXT_PUBLIC_REFRESH_INTERVAL=5000
```

4. Run the development server:

```bash
npm run dev
```

Your dashboard will be available at [http://localhost:3000](http://localhost:3000)

## 🏗️ Project Structure

```
ai-employee-dashboard/
├── public/                 # Static assets
├── src/
│   ├── app/               # Next.js App Router pages
│   │   ├── api/           # API routes for data fetching
│   │   ├── layout.tsx     # Main layout
│   │   └── page.tsx       # Dashboard home page
│   ├── components/        # Reusable UI components
│   │   ├── dashboard/     # Dashboard-specific components
│   │   ├── charts/        # Chart components
│   │   ├── ui/           # Base UI components
│   │   └── providers/    # Context providers
│   ├── lib/              # Utility functions
│   └── types/            # Type definitions
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

## 🔧 Configuration

The dashboard connects to your AI_Employee_Vault by reading files from:

- `Needs_Action/` - For pending tasks and emails
- `Plans/` - For in-progress tasks
- `Done/` - For completed tasks
- `Pending_Approval/` - For approval requests

Make sure your `VAULT_PATH` environment variable correctly points to your vault directory.

## 📊 Data Flow

1. **API Routes** (`src/app/api/`) read markdown files from your vault
2. **Components** fetch data using React hooks
3. **UI Elements** display the data with beautiful visualizations
4. **Real-time Updates** refresh data every 5 seconds

## 🎨 Customization

### Colors
Edit `tailwind.config.js` to customize the color palette:

```js
colors: {
  background: '#0A0A0F',           // Deep space black
  surface: '#141419',              // Card background
  surface-elevated: '#1C1C23',     // Elevated cards
  // ... more colors
}
```

### Typography
Update fonts in `src/app/layout.tsx`:

```tsx
import { Inter, JetBrains_Mono } from 'next/font/google';
```

## 🚀 Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel --prod
```

### Node.js Production
```bash
npm run build
npm start
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use and modify for your personal or commercial projects.

## 🆘 Support

If you encounter any issues:

1. Check the console for error messages
2. Verify your `VAULT_PATH` is correct
3. Ensure your vault directory structure matches the expected format
4. Open an issue in the repository

---

Built with ❤️ for your Personal AI Employee project