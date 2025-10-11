"use client";

import NavbarFinal from "@/components/navbar";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";

export default function Login() {
  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Background musical instruments with neon effect */}
      <div className="absolute inset-0 z-0">
        {/* Accordion - bottom left */}
        <div className="absolute bottom-20 left-10 opacity-30">
          <Image
            src="/images/login-accordion.png"
            alt="Accordion"
            width={120}
            height={120}
            className="filter drop-shadow-[0_0_10px_rgba(0,255,0,0.5)]"
          />
        </div>

        {/* Violin - far left */}
        <div className="absolute top-20 left-5 opacity-30">
          <Image
            src="/images/login-violin.png"
            alt="Violin"
            width={100}
            height={100}
            className="filter drop-shadow-[0_0_10px_rgba(255,0,150,0.5)]"
          />
        </div>

        {/* Guitar - top center */}
        <div className="absolute top-10 left-1/2 transform -translate-x-1/2 opacity-30">
          <Image
            src="/images/login-guitar.png"
            alt="Guitar"
            width={120}
            height={120}
            className="filter drop-shadow-[0_0_10px_rgba(150,0,255,0.5)]"
          />
        </div>

        {/* Saxophone - right side */}
        <div className="absolute top-32 right-40 opacity-30">
          <Image
            src="/images/login-sax.png"
            alt="Saxophone"
            width={100}
            height={100}
            className="filter drop-shadow-[0_0_10px_rgba(255,215,0,0.5)]"
          />
        </div>

        {/* Trumpet - below saxophone */}
        <div className="absolute top-60 right-36 opacity-30">
          <Image
            src="/images/login-trumpete.png"
            alt="Trumpet"
            width={80}
            height={80}
            className="filter drop-shadow-[0_0_10px_rgba(255,215,0,0.5)]"
          />
        </div>

        {/* Flute - bottom right */}
        <div className="absolute bottom-32 right-20 opacity-30">
          <Image
            src="/images/login-flute.png"
            alt="Flute"
            width={100}
            height={100}
            className="filter drop-shadow-[0_0_10px_rgba(0,255,255,0.5)]"
          />
        </div>

        {/* Tambourine - bottom center */}
        <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2 opacity-30">
          <Image
            src="/images/login-pandero.png"
            alt="Tambourine"
            width={80}
            height={80}
            className="filter drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]"
          />
        </div>
      </div>

      <div className="relative z-10 flex min-h-screen">
        {/* Left side - Login Form */}
        <div className="flex-1 flex items-center justify-center p-8">
          <Card className="w-full max-w-md bg-white/95 backdrop-blur-sm shadow-2xl p-8 rounded-xl">
            <div className="space-y-6">
              <div className="text-center">
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                  Welcome Back
                </h1>
                <p className="text-gray-600">Sign in to your account</p>
              </div>

              <div className="space-y-4">
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Email
                  </label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="Enter your email"
                    className="w-full"
                  />
                </div>

                <div>
                  <label
                    htmlFor="password"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Password
                  </label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Enter your password"
                    className="w-full"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="remember"
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    defaultChecked
                  />
                  <label
                    htmlFor="remember"
                    className="ml-2 block text-sm text-gray-700"
                  >
                    Remember me
                  </label>
                </div>
                <a
                  href="/forgot-password"
                  className="text-sm text-blue-600 hover:text-blue-500 underline"
                >
                  Forgot password?
                </a>
              </div>

              <div className="space-y-3">
                <Button className="w-full bg-gray-800 hover:bg-gray-700 text-white">
                  Sign In
                </Button>
                <Button
                  variant="outline"
                  className="w-full border-gray-300 text-gray-500"
                >
                  Create Account
                </Button>
              </div>

              <div className="text-center">
                <p className="text-sm text-gray-600 mb-3">login with</p>
                <div className="flex justify-center space-x-4">
                  <button
                    type="button"
                    className="p-2 rounded-full bg-white shadow-md hover:shadow-lg transition-shadow"
                  >
                    <Image
                      src="https://developers.google.com/identity/images/g-logo.png"
                      alt="Google"
                      width={24}
                      height={24}
                    />
                  </button>
                  <button
                    type="button"
                    className="p-2 rounded-full bg-blue-600 text-white hover:bg-blue-700 transition-colors"
                  >
                    <svg
                      className="w-6 h-6"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                      aria-label="Facebook"
                    >
                      <title>Facebook</title>
                      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                    </svg>
                  </button>
                  <button
                    type="button"
                    className="p-2 rounded-full bg-black text-white hover:bg-gray-800 transition-colors"
                  >
                    <svg
                      className="w-6 h-6"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                      aria-label="Apple"
                    >
                      <title>Apple</title>
                      <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Right side - Logo */}
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="relative">
            <Image
              src="/images/logo-png.png"
              alt="Musician AI Logo"
              width={400}
              height={400}
              className="drop-shadow-2xl"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
