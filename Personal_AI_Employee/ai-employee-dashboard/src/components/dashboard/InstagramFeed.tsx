'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Instagram, Heart, MessageCircle, Share } from 'lucide-react';

interface InstagramPost {
  id: string;
  caption: string;
  imageUrl: string;
  likes: number;
  comments: number;
  timestamp: string;
  engagementRate: number;
}

export default function InstagramFeed() {
  const [posts, setPosts] = useState<InstagramPost[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching Instagram posts
    const fetchInstagramPosts = async () => {
      try {
        setLoading(true);

        // Simulated Instagram data
        const mockData: InstagramPost[] = [
          {
            id: 'post1',
            caption: 'Just launched our new product! Check out the features that make us stand out in the market 🚀 #innovation #productlaunch',
            imageUrl: '/placeholder-instagram-1.jpg',
            likes: 342,
            comments: 24,
            timestamp: '2 hours ago',
            engagementRate: 4.2
          },
          {
            id: 'post2',
            caption: 'Behind the scenes of our team working on the next big feature. Passion and dedication drive innovation! #teamwork #devlife',
            imageUrl: '/placeholder-instagram-2.jpg',
            likes: 289,
            comments: 18,
            timestamp: '1 day ago',
            engagementRate: 3.8
          },
          {
            id: 'post3',
            caption: 'Celebrating another successful client project! Their success is our success. #clientsuccess #results',
            imageUrl: '/placeholder-instagram-3.jpg',
            likes: 456,
            comments: 32,
            timestamp: '2 days ago',
            engagementRate: 5.1
          }
        ];

        setPosts(mockData);
      } catch (error) {
        console.error('Error fetching Instagram posts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchInstagramPosts();
  }, []);

  if (loading) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Instagram className="w-5 h-5" />
            Instagram Feed
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-48 bg-gray-200 rounded-md mb-3"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Instagram className="w-5 h-5" />
          Instagram Feed
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {posts.map((post) => (
            <div key={post.id} className="border-b pb-4 last:border-b-0 last:pb-0">
              <div className="relative mb-3">
                <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full h-48" />
              </div>
              <p className="text-sm mb-2 line-clamp-3">{post.caption}</p>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-1">
                    <Heart className="w-4 h-4" />
                    <span>{post.likes}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <MessageCircle className="w-4 h-4" />
                    <span>{post.comments}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span>ER: {post.engagementRate}%</span>
                  <span>{post.timestamp}</span>
                </div>
              </div>
            </div>
          ))}

          <button className="w-full py-2 text-center text-sm text-blue-600 hover:text-blue-800 font-medium">
            View More on Instagram
          </button>
        </div>
      </CardContent>
    </Card>
  );
}