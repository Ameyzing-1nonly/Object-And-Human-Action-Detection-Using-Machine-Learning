import Header from '@/components/custom/Header';
import { UserButton } from '@clerk/clerk-react';
import { Camera, Video, Activity, PlayCircle } from 'lucide-react';
import React from 'react';

function Home() {
  return (
    <div>
      <Header />
      <div>
        {/* Hero Section */}
        <section className="z-50">
          <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16 lg:px-12">
            <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
              Object Detection & <span className="text-primary">Human Action Recognition</span>
            </h1>
            <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400">
              Run state-of-the-art AI models to detect objects and recognize human activities in videos and live feeds.
            </p>
            <div className="flex flex-col mb-8 lg:mb-16 space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
              <a
                href="/dashboard"
                className="inline-flex justify-center items-center py-3 px-5 text-base font-medium text-center text-white rounded-lg bg-primary hover:bg-primary-dark focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900"
              >
                Get Started
                <svg className="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </a>
              <a
                href="https://youtu.be/Q5LM985yUmQ"
                className="inline-flex justify-center items-center py-3 px-5 text-base font-medium text-center text-gray-900 rounded-lg border border-gray-300 hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-gray-700 dark:hover:bg-gray-700 dark:focus:ring-gray-800"
              >
                <svg className="mr-2 -ml-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
                </svg>
                Watch Demo
              </a>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-8 bg-white z-50 px-4 mx-auto max-w-screen-xl text-center lg:py-16 lg:px-12">
          <h2 className="font-bold text-3xl">How It Works?</h2>
          <h2 className="text-md text-gray-500">Perform object detection & action recognition in 3 easy steps</h2>

          <div className="mt-8 grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
            {/* Step 1: Select Model */}
            <div className="block rounded-xl border bg-white border-gray-200 p-8 shadow-xl transition hover:border-blue-500/10 hover:shadow-blue-500/10">
              <Camera className="h-8 w-8 text-primary" />
              <h2 className="mt-4 text-xl font-bold text-black">Choose Input Type</h2>
              <p className="mt-1 text-sm text-gray-600">
                Select whether to analyze an image, video, or live camera feed.
              </p>
            </div>

            {/* Step 2: Run Detection */}
            <div className="block rounded-xl border bg-white border-gray-200 p-8 shadow-xl transition hover:border-green-500/10 hover:shadow-green-500/10">
              <Activity className="h-8 w-8 text-primary" />
              <h2 className="mt-4 text-xl font-bold text-black">Run AI Models</h2>
              <p className="mt-1 text-sm text-gray-600">
                Our pre-trained deep learning models will analyze your input in real-time.
              </p>
            </div>

            {/* Step 3: Get Results */}
            <div className="block rounded-xl border bg-white border-gray-200 p-8 shadow-xl transition hover:border-red-500/10 hover:shadow-red-500/10">
              <PlayCircle className="h-8 w-8 text-primary" />
              <h2 className="mt-4 text-xl font-bold text-black">View Results</h2>
              <p className="mt-1 text-sm text-gray-600">
                Get real-time object detection and human action recognition results.
              </p>
            </div>
          </div>

          {/* CTA Button */}
          <div className="mt-12 text-center">
            <a
              href="/dashboard"
              className="inline-block rounded bg-primary px-12 py-3 text-sm font-medium text-white transition hover:bg-primary-dark focus:outline-none focus:ring focus:ring-yellow-400"
            >
              Try Now
            </a>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Home;
