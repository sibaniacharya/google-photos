import React, { useState, useEffect } from 'react';

export default function App() {
  const [currentRoute, setCurrentRoute] = useState(() => {
    const hash = window.location.hash.replace('#', '');
    return hash || 'overview';
  });

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#', '');
      setCurrentRoute(hash || 'overview');
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const navigate = (route) => {
    window.location.hash = route;
  };

  const navItems = [
    { label: 'Overview', route: 'overview' },
    { label: 'Discovery', route: 'discovery' },
    { label: 'Confirmed Evidence', route: 'confirmed' },
    { label: 'Opportunity', route: 'opportunity' },
    { label: 'Audit', route: 'audit' },
    { label: 'Methodology', route: 'methodology' },
    { label: 'Run Engine', route: 'run-engine' }
  ];

  const filterPills = [
    { label: 'All reviews', count: '2,022', route: 'all-reviews' },
    { label: 'High-recall', count: '300', route: 'high-recall' },
    { label: 'AI TRUE', count: '6', route: 'ai-true' },
    { label: 'Confirmed', count: '1', route: 'confirmed' },
    { label: 'Ambiguous', count: '2', route: 'ambiguous' },
    { label: 'Excluded', count: '3', route: 'excluded' },
  ];

  return (
    <div className="min-h-screen bg-white text-[#202124] font-sans selection:bg-blue-100 pb-16">
      
      {/* HEADER */}
      <header className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-[1440px] mx-auto px-4 md:px-8 h-16 flex items-center justify-between gap-4">
          
          <div className="flex items-center gap-3 shrink-0 cursor-pointer" onClick={() => navigate('overview')}>
            <div className="relative w-8 h-8 flex items-center justify-center shrink-0">
              <span className="absolute top-0 left-1.5 w-3.5 h-3.5 rounded-t-full rounded-bl-full bg-[#EA4335]"></span>
              <span className="absolute top-1.5 right-0 w-3.5 h-3.5 rounded-r-full rounded-tl-full bg-[#4285F4]"></span>
              <span className="absolute bottom-0 right-1.5 w-3.5 h-3.5 rounded-b-full rounded-tr-full bg-[#34A853]"></span>
              <span className="absolute bottom-1.5 left-0 w-3.5 h-3.5 rounded-l-full rounded-br-full bg-[#FBBC05]"></span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[22px] tracking-tight text-[#3c4043]">Photos Research</span>
              <span className="px-2 py-0.5 rounded-full bg-blue-50 text-[#1a73e8] text-[11px] uppercase tracking-wider font-semibold">Labs</span>
            </div>
          </div>

          <div className="flex-1 max-w-[720px] hidden md:block px-4">
            <div className="h-12 w-full bg-[#f1f3f4] focus-within:bg-white focus-within:shadow-md focus-within:border-transparent border border-transparent transition-all rounded-full flex items-center px-4 gap-3 text-gray-600">
              <span className="material-symbols-outlined text-[24px]">search</span>
              <input 
                className="w-full bg-transparent border-none outline-none text-base text-gray-800 placeholder:text-gray-500" 
                placeholder="Search research evidence, timestamps, faces, transcripts..." 
                type="text"
              />
              <button className="p-1.5 rounded-full hover:bg-gray-200 transition-colors flex items-center justify-center">
                <span className="material-symbols-outlined text-[20px]">mic</span>
              </button>
              <kbd className="hidden lg:inline-flex items-center px-2 py-1 text-[11px] font-medium text-gray-500 bg-white border border-gray-200 rounded-md shadow-sm">Ctrl K</kbd>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0 text-gray-600">
            <button className="p-2 rounded-full hover:bg-gray-100 transition-colors flex items-center justify-center">
              <span className="material-symbols-outlined text-[24px]">help</span>
            </button>
            <button className="p-2 rounded-full hover:bg-gray-100 transition-colors flex items-center justify-center">
              <span className="material-symbols-outlined text-[24px]">settings</span>
            </button>
            <button className="p-2 rounded-full hover:bg-gray-100 transition-colors flex items-center justify-center">
              <span className="material-symbols-outlined text-[24px]">apps</span>
            </button>
            <button className="w-8 h-8 ml-2 rounded-full bg-[#1a73e8] text-white flex items-center justify-center font-medium text-sm border-2 border-white shadow-sm hover:shadow-md transition-shadow">
              U
            </button>
          </div>
        </div>
        
        {/* NAVIGATION */}
        <div className="max-w-[1440px] mx-auto px-4 md:px-8 h-12 flex items-center gap-6 overflow-x-auto">
          {navItems.map(item => (
            <button 
              key={item.route}
              onClick={() => navigate(item.route)}
              className={`h-full border-b-2 px-1 text-[14px] font-medium transition-colors whitespace-nowrap ${
                currentRoute === item.route 
                  ? 'border-[#1a73e8] text-[#1a73e8]' 
                  : 'border-transparent text-[#5f6368] hover:text-[#202124]'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
      </header>

      {/* FILTER BAR */}
      <div className="bg-white border-b border-gray-100 sticky top-[112px] z-40 bg-opacity-95 backdrop-blur-sm shadow-sm">
        <div className="max-w-[1440px] mx-auto px-4 md:px-8 py-3 flex items-center gap-2 overflow-x-auto">
          {filterPills.map(filter => {
            const isActive = currentRoute === filter.route;
            return (
              <button 
                key={filter.route}
                onClick={() => navigate(filter.route)}
                className={`h-8 px-4 rounded-full text-[13px] font-medium border flex items-center gap-2 whitespace-nowrap transition-colors ${
                  isActive 
                    ? 'bg-[#1a73e8] text-white border-transparent shadow-sm' 
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 hover:shadow-sm'
                }`}
              >
                {isActive && <span className="material-symbols-outlined text-[16px]">check</span>}
                <span>{filter.label}</span>
                <span className={`text-[11px] ${isActive ? 'text-blue-100' : 'text-gray-500'}`}>{filter.count}</span>
              </button>
            );
          })}
        </div>
      </div>

      <main className="max-w-[1440px] mx-auto px-4 md:px-8 py-10 flex flex-col gap-12">

        {/* ==============================================================
            OVERVIEW TAB
            ============================================================== */}
        {currentRoute === 'overview' && (
          <section className="flex flex-col gap-12">
            <div>
              <h2 className="text-[28px] font-normal text-[#202124] mb-4">Discovery Engine Part 1</h2>
              <p className="text-[#5f6368] max-w-3xl leading-relaxed text-lg">
                Part 1 establishes one verified retrieval problem from an audited public-review corpus. The confirmed sample is too small to estimate prevalence, failure rate, or category-level distribution.
              </p>
            </div>
            
            <div className="bg-[#f8f9fa] border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
              <div className="flex items-center gap-2 mb-6">
                <span className="material-symbols-outlined text-[#1a73e8]">account_tree</span>
                <h2 className="text-[18px] font-medium text-[#202124]">Research Pipeline</h2>
              </div>
              <div className="flex items-center gap-2 overflow-x-auto pb-4 pt-1 snap-x">
                <PipelineStage num="2,022" label="Real reviews" onClick={() => navigate('all-reviews')} clickable />
                <PipelineArrow />
                <PipelineStage num="300" label="High-recall candidates" onClick={() => navigate('high-recall')} clickable />
                <PipelineArrow />
                <PipelineStage num="300" label="AI extraction" onClick={() => navigate('ai-true')} clickable />
                <PipelineArrow />
                <PipelineStage num="300/300" label="Schema valid" />
                <PipelineArrow />
                <PipelineStage num="294/300" label="Automated validation" />
                <PipelineArrow />
                <PipelineStage num="6" label="AI TRUE" onClick={() => navigate('ai-true')} clickable />
                <PipelineArrow />
                <div 
                  onClick={() => navigate('confirmed')}
                  className="flex-shrink-0 bg-[#e8f0fe] border border-[#d2e3fc] rounded-2xl p-4 min-w-[140px] flex flex-col items-center text-center snap-start shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                >
                  <span className="text-2xl font-normal text-[#1a73e8] mb-1">1</span>
                  <span className="text-[13px] font-medium text-[#1967d2] leading-tight">Confirmed</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div onClick={() => navigate('discovery')} className="cursor-pointer bg-white border border-gray-200 rounded-3xl p-6 shadow-sm hover:shadow-md transition-shadow">
                <span className="material-symbols-outlined text-[#1a73e8] text-[32px] mb-4">manage_search</span>
                <h3 className="text-xl font-medium text-[#202124] mb-2">Discovery Approach</h3>
                <p className="text-[#5f6368] mb-4">View how 2,022 reviews were distilled to 1 confirmed case through rigorous semantic extraction and human audit.</p>
                <span className="text-[#1a73e8] font-medium text-sm flex items-center gap-1">View Discovery <span className="material-symbols-outlined text-[16px]">arrow_forward</span></span>
              </div>
              <div onClick={() => navigate('confirmed')} className="cursor-pointer bg-white border border-gray-200 rounded-3xl p-6 shadow-sm hover:shadow-md transition-shadow">
                <span className="material-symbols-outlined text-[#188038] text-[32px] mb-4">verified</span>
                <h3 className="text-xl font-medium text-[#202124] mb-2">Confirmed Evidence</h3>
                <p className="text-[#5f6368] mb-4">Explore the detailed breakdown of our single manually confirmed retrieval gap case.</p>
                <span className="text-[#1a73e8] font-medium text-sm flex items-center gap-1">View Evidence <span className="material-symbols-outlined text-[16px]">arrow_forward</span></span>
              </div>
            </div>
          </section>
        )}

        {/* ==============================================================
            FILTER PAGES
            ============================================================== */}
        
        {/* ALL REVIEWS */}
        {currentRoute === 'all-reviews' && (
          <section className="flex flex-col gap-6">
            <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-4">
                <span className="material-symbols-outlined text-[#1a73e8] text-[28px]">reviews</span>
                <h2 className="text-[24px] font-medium text-[#202124]">2,022 Total Reviews</h2>
              </div>
              <p className="text-[#5f6368] text-[16px] max-w-3xl mb-6">
                Source/public-review corpus. Do not imply that all 2,022 are retrieval-problem evidence. This is the raw unfiltered ingest pool.
              </p>
              <div className="h-12 w-full max-w-2xl bg-[#f8f9fa] border border-gray-200 rounded-full flex items-center px-4 gap-3 text-gray-500 mb-6">
                <span className="material-symbols-outlined text-[20px]">search</span>
                <input className="w-full bg-transparent border-none outline-none text-sm text-gray-800" placeholder="Search the full 2,022 review corpus..." type="text" />
              </div>
              <div className="bg-[#f8f9fa] p-8 rounded-2xl border border-gray-200 flex flex-col items-center text-center">
                <span className="material-symbols-outlined text-gray-400 text-[48px] mb-4">inventory_2</span>
                <p className="text-gray-500 font-medium">Corpus view available in full application.</p>
              </div>
            </div>
          </section>
        )}

        {/* HIGH RECALL */}
        {currentRoute === 'high-recall' && (
          <section className="flex flex-col gap-6">
            <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-4">
                <span className="material-symbols-outlined text-[#1a73e8] text-[28px]">filter_alt</span>
                <h2 className="text-[24px] font-medium text-[#202124]">300 High-Recall Candidates</h2>
              </div>
              <p className="text-[#5f6368] text-[16px] max-w-3xl mb-2">
                These candidates were selected for high recall before semantic classification. 
              </p>
              <p className="text-[#d93025] font-medium text-[15px] mb-6">
                They are NOT confirmed retrieval problems.
              </p>
              <div className="bg-[#f8f9fa] p-8 rounded-2xl border border-gray-200 flex flex-col items-center text-center">
                <span className="material-symbols-outlined text-gray-400 text-[48px] mb-4">format_list_bulleted</span>
                <p className="text-gray-500 font-medium">Candidate list view available in full application.</p>
              </div>
            </div>
          </section>
        )}

        {/* AI TRUE */}
        {currentRoute === 'ai-true' && (
          <section className="flex flex-col gap-6">
            <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-4">
                <span className="material-symbols-outlined text-[#1a73e8] text-[28px]">psychology</span>
                <h2 className="text-[24px] font-medium text-[#202124]">6 AI TRUE Candidates</h2>
              </div>
              <div className="bg-[#fef7e0] border border-[#fce8b2] rounded-xl p-4 mb-6">
                <p className="text-[#b06000] font-medium text-[15px]">
                  Clearly label them as AI-classified candidates, NOT confirmed evidence.
                </p>
              </div>
              <p className="text-[#5f6368] text-[16px] max-w-3xl mb-6">
                These 6 records were classified as AI TRUE by the Groq semantic extraction stage. They have undergone manual audit.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="border border-blue-200 bg-blue-50/30 rounded-2xl p-5 flex flex-col cursor-pointer hover:shadow-md transition-shadow" onClick={() => navigate('confirmed')}>
                  <span className="text-blue-700 font-semibold mb-3 flex items-center gap-2"><span className="material-symbols-outlined text-[18px]">verified</span> Confirmed (1)</span>
                  <span className="font-mono text-sm bg-white border border-blue-100 px-2 py-1 rounded w-fit text-blue-800">fd8a8056</span>
                </div>
                <div className="border border-amber-200 bg-amber-50/30 rounded-2xl p-5 flex flex-col cursor-pointer hover:shadow-md transition-shadow" onClick={() => navigate('ambiguous')}>
                  <span className="text-amber-700 font-semibold mb-3 flex items-center gap-2"><span className="material-symbols-outlined text-[18px]">help</span> Ambiguous (2)</span>
                  <div className="flex flex-col gap-2">
                    <span className="font-mono text-sm bg-white border border-amber-100 px-2 py-1 rounded w-fit text-amber-800">43ac5ac2</span>
                    <span className="font-mono text-sm bg-white border border-amber-100 px-2 py-1 rounded w-fit text-amber-800">7a81912f</span>
                  </div>
                </div>
                <div className="border border-gray-200 bg-gray-50/50 rounded-2xl p-5 flex flex-col cursor-pointer hover:shadow-md transition-shadow" onClick={() => navigate('excluded')}>
                  <span className="text-gray-700 font-semibold mb-3 flex items-center gap-2"><span className="material-symbols-outlined text-[18px]">cancel</span> Excluded (3)</span>
                  <div className="flex flex-col gap-2">
                    <span className="font-mono text-sm bg-white border border-gray-200 px-2 py-1 rounded w-fit text-gray-800">c34312c4</span>
                    <span className="font-mono text-sm bg-white border border-gray-200 px-2 py-1 rounded w-fit text-gray-800">94aa2507</span>
                    <span className="font-mono text-sm bg-white border border-gray-200 px-2 py-1 rounded w-fit text-gray-800">98034214</span>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* AMBIGUOUS */}
        {currentRoute === 'ambiguous' && (
          <section className="flex flex-col gap-6">
            <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-4">
                <span className="material-symbols-outlined text-[#f29900] text-[28px]">help</span>
                <h2 className="text-[24px] font-medium text-[#202124]">2 Ambiguous Cases</h2>
              </div>
              <p className="text-[#5f6368] text-[16px] max-w-3xl mb-8">
                These cases are retained for transparency but excluded from opportunity claims.
              </p>
              
              <div className="flex flex-col gap-6">
                <div className="bg-[#fef7e0] border border-[#fce8b2] rounded-2xl p-6">
                  <span className="font-mono text-[14px] font-bold bg-white text-[#b06000] px-3 py-1 rounded-md border border-[#fce8b2] mb-3 inline-block">43ac5ac2</span>
                  <p className="text-[#8d4e00] text-[16px] leading-relaxed">
                    “I can't find my oldest photo” is insufficient to distinguish incomplete-memory retrieval from a request for oldest-first sorting.
                  </p>
                </div>
                <div className="bg-[#fef7e0] border border-[#fce8b2] rounded-2xl p-6">
                  <span className="font-mono text-[14px] font-bold bg-white text-[#b06000] px-3 py-1 rounded-md border border-[#fce8b2] mb-3 inline-block">7a81912f</span>
                  <p className="text-[#8d4e00] text-[16px] leading-relaxed">
                    Phone-to-phone transfer context makes it unclear whether photos were present but difficult to retrieve or simply failed to sync/backup.
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* EXCLUDED */}
        {currentRoute === 'excluded' && (
          <section className="flex flex-col gap-6">
            <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-4">
                <span className="material-symbols-outlined text-gray-500 text-[28px]">cancel</span>
                <h2 className="text-[24px] font-medium text-[#202124]">3 Excluded Cases</h2>
              </div>
              <p className="text-[#5f6368] text-[16px] max-w-3xl mb-8">
                These cases were excluded. The audit explanations are provided below.
              </p>
              
              <div className="flex flex-col gap-6">
                <div className="bg-[#f8f9fa] border border-gray-200 rounded-2xl p-6">
                  <span className="font-mono text-[14px] font-bold bg-white text-gray-700 px-3 py-1 rounded-md border border-gray-200 mb-3 inline-block">c34312c4</span>
                  <p className="text-gray-700 text-[16px] leading-relaxed">
                    Physical photograph was described as misplaced; failed digital retrieval in Google Photos was not established.
                  </p>
                </div>
                <div className="bg-[#f8f9fa] border border-gray-200 rounded-2xl p-6">
                  <span className="font-mono text-[14px] font-bold bg-white text-gray-700 px-3 py-1 rounded-md border border-gray-200 mb-3 inline-block">94aa2507</span>
                  <p className="text-gray-700 text-[16px] leading-relaxed">
                    Generic UI/layout complaint; incomplete-memory retrieval was not established.
                  </p>
                </div>
                <div className="bg-[#f8f9fa] border border-gray-200 rounded-2xl p-6">
                  <span className="font-mono text-[14px] font-bold bg-white text-gray-700 px-3 py-1 rounded-md border border-gray-200 mb-3 inline-block">98034214</span>
                  <p className="text-gray-700 text-[16px] leading-relaxed">
                    Known lost-photo/data-recovery attempt; incomplete-memory retrieval was not established.
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* ==============================================================
            CORE TABS
            ============================================================== */}

        {/* DISCOVERY TAB */}
        {currentRoute === 'discovery' && (
          <section className="flex flex-col gap-8">
            <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <span className="material-symbols-outlined text-[#1a73e8]">account_tree</span>
                <h2 className="text-[22px] font-medium text-[#202124]">Research Pipeline</h2>
              </div>
              <p className="text-[#5f6368] max-w-3xl mb-8 text-[16px]">
                High-recall candidate discovery intentionally prioritized recall before semantic classification to ensure no potential targets were missed.
              </p>
              
              <div className="flex items-center gap-2 overflow-x-auto pb-4 pt-1 snap-x">
                <PipelineStage num="2,022" label="Real reviews" onClick={() => navigate('all-reviews')} clickable />
                <PipelineArrow />
                <PipelineStage num="300" label="High-recall candidates" onClick={() => navigate('high-recall')} clickable />
                <PipelineArrow />
                <PipelineStage num="300" label="AI extraction" onClick={() => navigate('ai-true')} clickable />
                <PipelineArrow />
                <PipelineStage num="300/300" label="Schema valid" />
                <PipelineArrow />
                <PipelineStage num="294/300" label="Automated validation" />
                <PipelineArrow />
                <PipelineStage num="6" label="AI TRUE" onClick={() => navigate('ai-true')} clickable />
                <PipelineArrow />
                <div 
                  onClick={() => navigate('confirmed')}
                  className="flex-shrink-0 bg-[#e8f0fe] border border-[#d2e3fc] rounded-2xl p-4 min-w-[140px] flex flex-col items-center text-center snap-start shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                >
                  <span className="text-2xl font-normal text-[#1a73e8] mb-1">1</span>
                  <span className="text-[13px] font-medium text-[#1967d2] leading-tight">Confirmed</span>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* CONFIRMED EVIDENCE TAB */}
        {currentRoute === 'confirmed' && (
          <div className="flex flex-col gap-12">
            
            <section>
              <div className="bg-[#f8f9fa] border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex flex-wrap items-center gap-3 mb-6 pb-4 border-b border-gray-200">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#e8f0fe] text-[#1967d2] text-xs font-semibold tracking-wide border border-[#d2e3fc]">
                    <span className="material-symbols-outlined text-[16px]">verified</span>
                    1 CONFIRMED
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white text-gray-700 text-xs font-mono border border-gray-200">
                    Record fd8a8056
                  </span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full bg-white text-gray-500 text-xs border border-gray-200">
                    Audited evidence
                  </span>
                </div>

                <h1 className="text-2xl md:text-[28px] font-normal text-[#202124] mb-8 leading-snug">
                  User cannot locate previously uploaded old photos that are personally meaningful.
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-white rounded-2xl p-5 md:p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-2 mb-4">
                      <span className="material-symbols-outlined text-[#188038] text-[20px]">psychology</span>
                      <h3 className="text-[13px] font-semibold text-gray-800 uppercase tracking-wider">What the user remembers</h3>
                    </div>
                    <ul className="space-y-3">
                      <CheckItem text="Old photos uploaded a long time ago" />
                      <CheckItem text="Photos represent meaningful memories" />
                      <CheckItem text="User believes they did not delete them" />
                    </ul>
                  </div>

                  <div className="bg-white rounded-2xl p-5 md:p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-2 mb-4">
                      <span className="material-symbols-outlined text-[#d93025] text-[20px]">help</span>
                      <h3 className="text-[13px] font-semibold text-gray-800 uppercase tracking-wider">What is unknown</h3>
                    </div>
                    <ul className="space-y-3">
                      <QuestionItem text="Current location of the specific photos" />
                      <QuestionItem text="No specific search query stated" />
                      <QuestionItem text="No search strategy stated" />
                    </ul>
                  </div>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-[13px] font-semibold text-gray-800 uppercase tracking-wider mb-4">Memory → Search Gap</h2>
              <div className="flex flex-col md:flex-row items-center gap-2 md:gap-4 overflow-x-auto pb-4">
                <FlowStep num="1" title="Memory" desc="Old + meaningful photos" />
                <FlowArrow />
                <FlowStep num="2" title="Search gap" desc="No specific searchable details or search strategy stated" />
                <FlowArrow />
                <FlowStep num="3" title="Retrieval outcome" desc="Unable to find photos" />
                <FlowArrow />
                <FlowStep num="4" title="User perception" desc="User believes the images were removed automatically" />
                <FlowArrow />
                <div className="flex-1 w-full min-w-[200px] bg-[#fce8e6] border border-[#fad2cf] rounded-2xl p-4 flex flex-col items-center text-center shadow-sm hover:shadow-md transition-shadow">
                  <span className="w-6 h-6 rounded-full bg-white text-[#d93025] flex items-center justify-center font-bold text-xs mb-2 shadow-sm">5</span>
                  <span className="text-sm font-semibold text-[#b31412] mb-1">User-stated trust impact</span>
                  <span className="text-[13px] text-[#c5221f] leading-snug">The user explicitly states that this has made them unable to trust Google.</span>
                </div>
              </div>
            </section>

            <section>
              <div className="bg-white border border-[#d2e3fc] rounded-3xl p-6 md:p-8 relative shadow-sm hover:shadow-md transition-shadow overflow-hidden">
                <span className="material-symbols-outlined text-[80px] text-[#e8f0fe] absolute top-4 right-6 select-none z-0">format_quote</span>
                
                <div className="relative z-10">
                  <span className="text-[11px] font-bold text-[#1a73e8] uppercase tracking-widest mb-3 block">USER EVIDENCE</span>
                  <blockquote className="text-[20px] md:text-[24px] text-[#202124] font-normal leading-relaxed mb-8 max-w-4xl">
                    “while trying to find some old pics which already uploaded a long time ago, I can't find them now”
                  </blockquote>
                  
                  <div className="flex flex-wrap items-center gap-2 pt-5 border-t border-gray-100">
                    <EvidenceMeta label="Record" value="fd8a8056" isMono />
                    <EvidenceMeta label="Retrieval category" value="Episodic / old-memory retrieval" />
                    <EvidenceMeta label="Outcome" value="Failure to find pictures" />
                    <EvidenceMeta label="Search strategy" value="Unknown / not stated" />
                  </div>
                </div>
              </div>
            </section>
            
            {/* INCLUDED IN CONFIRMED PAGE PER REQUEST */}
            <OpportunitySection />
            <AuditSection />
            <MethodologySection />
          </div>
        )}

        {/* OPPORTUNITY TAB */}
        {currentRoute === 'opportunity' && <OpportunitySection />}

        {/* AUDIT TAB */}
        {currentRoute === 'audit' && <AuditSection />}

        {/* METHODOLOGY TAB */}
        {currentRoute === 'methodology' && <MethodologySection />}

        {/* RUN ENGINE TAB */}
        {currentRoute === 'run-engine' && <RunEngineSection />}

      </main>
    </div>
  );
}

/* HELPER SECTION COMPONENTS */

function RunEngineSection() {
  const [inputText, setInputText] = useState(`{"record_id": "demo-1", "review_text": "I can't find my old photos"}`);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleRunEngine = async () => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);
      
      let records = [];
      try {
        const parsed = JSON.parse(inputText);
        records = Array.isArray(parsed) ? parsed : [parsed];
      } catch (err) {
        throw new Error("Invalid JSON input. Please provide a valid JSON array or object.");
      }

      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE}/api/ai/extract`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ records })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'API request failed');
      }

      setResult(data.extracted);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const checkHealth = async () => {
    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const res = await fetch(`${API_BASE}/health`);
      if (res.ok) alert("Backend is healthy!");
      else alert("Backend returned error.");
    } catch (e) {
      alert("Failed to connect to backend: " + e.message);
    }
  };

  return (
    <section>
      <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
        <div className="flex items-center gap-2 mb-3">
          <span className="material-symbols-outlined text-[#1a73e8] text-[24px]">terminal</span>
          <span className="text-[11px] font-bold text-gray-800 uppercase tracking-widest">DYNAMIC AI ENGINE TEST</span>
        </div>
        
        <p className="text-[#5f6368] mb-6">
          This tab dynamically executes the AI Engine deployed on Railway. The dashboard above is powered by the static, audited evidence from Part 1. 
          Use this to test new candidates.
        </p>

        <div className="mb-4">
          <label className="block text-sm font-semibold text-gray-700 mb-2">Input Candidates (JSON array or object):</label>
          <textarea 
            className="w-full h-40 p-4 border border-gray-300 rounded-xl font-mono text-sm"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
        </div>

        <div className="flex gap-4 mb-8">
          <button 
            onClick={handleRunEngine}
            disabled={loading}
            className="px-6 py-2 bg-[#1a73e8] text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Running AI Engine...' : 'Run Extract'}
          </button>
          <button 
            onClick={checkHealth}
            className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200"
          >
            Check Backend Health
          </button>
        </div>

        {error && (
          <div className="bg-[#fce8e6] text-[#c5221f] p-4 rounded-xl border border-[#fad2cf] mb-6">
            <h4 className="font-bold text-sm mb-1">Error executing AI Engine</h4>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {result && (
          <div>
            <h3 className="text-sm font-semibold text-gray-800 uppercase tracking-wider mb-2">Extraction Results</h3>
            <pre className="bg-[#f8f9fa] p-4 border border-gray-200 rounded-xl font-mono text-xs overflow-x-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </section>
  );
}

function OpportunitySection() {
  return (
    <section>
      <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm hover:shadow-md transition-shadow">
        <div className="flex items-center gap-2 mb-3">
          <span className="material-symbols-outlined text-[#fbbc04] text-[24px]">lightbulb</span>
          <span className="text-[11px] font-bold text-gray-800 uppercase tracking-widest">EVIDENCE-BACKED OPPORTUNITY AREA</span>
        </div>
        
        <h2 className="text-[20px] md:text-[24px] font-normal text-[#202124] mb-6 max-w-3xl leading-snug">
          Users may need better ways to locate or resurface older meaningful photos when they cannot provide precise search terms.
        </h2>
        
        <div className="flex flex-wrap gap-2">
          <span className="inline-flex items-center px-3 py-1.5 rounded-full bg-blue-50 text-[#1967d2] text-[13px] border border-[#d2e3fc] font-medium">
            Evidence status: Confirmed individual case
          </span>
          <span className="inline-flex items-center px-3 py-1.5 rounded-full bg-gray-50 text-gray-600 text-[13px] border border-gray-200 font-medium">
            Broader prevalence is NOT established
          </span>
          <span className="inline-flex items-center px-3 py-1.5 rounded-full bg-white text-gray-800 font-mono text-[13px] border border-gray-200 font-medium">
            Supporting record: fd8a8056
          </span>
        </div>
      </div>
    </section>
  );
}

function AuditSection() {
  return (
    <section>
      <div className="flex items-center gap-2 mb-4">
        <span className="material-symbols-outlined text-gray-600">fact_check</span>
        <h2 className="text-[22px] font-medium text-[#202124]">Audit Cohort</h2>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col h-full">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
            <span className="text-[13px] font-semibold text-[#1a73e8] uppercase tracking-wider">CONFIRMED — 1</span>
          </div>
          <div className="flex-1 space-y-4">
            <AuditItem 
              id="fd8a8056" 
              desc="Meaningful old photo retrieval failure resulting in explicit loss of system trust." 
              color="blue"
            />
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col h-full">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
            <span className="text-[13px] font-semibold text-[#f29900] uppercase tracking-wider">AMBIGUOUS — 2</span>
          </div>
          <div className="flex-1 space-y-4">
            <AuditItem 
              id="43ac5ac2" 
              desc="“I can't find my oldest photo” is insufficient to distinguish incomplete-memory retrieval from a request for oldest-first sorting." 
              color="amber"
            />
            <AuditItem 
              id="7a81912f" 
              desc="Phone-to-phone transfer context makes it unclear whether photos were present but difficult to retrieve or simply failed to sync/backup." 
              color="amber"
            />
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col h-full">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
            <span className="text-[13px] font-semibold text-gray-600 uppercase tracking-wider">EXCLUDED — 3</span>
          </div>
          <div className="flex-1 space-y-4">
            <AuditItem 
              id="c34312c4" 
              desc="Physical photograph was described as misplaced; failed digital retrieval in Google Photos was not established." 
              color="gray"
            />
            <AuditItem 
              id="94aa2507" 
              desc="Generic UI/layout complaint; incomplete-memory retrieval was not established." 
              color="gray"
            />
            <AuditItem 
              id="98034214" 
              desc="Known lost-photo/data-recovery attempt; incomplete-memory retrieval was not established." 
              color="gray"
            />
          </div>
        </div>
      </div>
    </section>
  );
}

function MethodologySection() {
  return (
    <section className="flex flex-col gap-8">
      <div className="bg-white border border-gray-200 rounded-3xl p-6 md:p-8 shadow-sm">
        <h2 className="text-[13px] font-semibold text-gray-800 uppercase tracking-wider mb-5">Methodology & Verification Pipeline</h2>
        
        <div className="flex flex-wrap items-center gap-2 mb-8">
          <MethodMetric num="2,022" label="Reviews collected" />
          <MethodMetric num="300" label="High-recall candidates" />
          <MethodMetric num="300" label="AI extraction" />
          <MethodMetric num="300/300" label="Schema-valid" />
          <MethodMetric num="294/300" label="Automated pass" />
          <MethodMetric num="6" label="AI TRUE" />
          <MethodMetric num="1" label="Confirmed" />
          <MethodMetric num="2" label="Ambiguous" />
          <MethodMetric num="3" label="Excluded" />
        </div>

        <h3 className="text-sm font-semibold text-gray-800 uppercase tracking-wider mb-4">Research Principles</h3>
        <ul className="space-y-4 mb-8 text-gray-700">
          <li className="flex items-start gap-3">
            <span className="material-symbols-outlined text-[#1a73e8] mt-0.5">check_circle</span>
            <span>AI candidate classification is not treated as final evidence.</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="material-symbols-outlined text-[#1a73e8] mt-0.5">check_circle</span>
            <span>Human/manual audit determines whether an AI TRUE candidate becomes confirmed evidence.</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="material-symbols-outlined text-[#1a73e8] mt-0.5">check_circle</span>
            <span>Confirmed evidence is based on the original user review text.</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="material-symbols-outlined text-[#1a73e8] mt-0.5">check_circle</span>
            <span>Ambiguous cases are retained but excluded from opportunity claims.</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="material-symbols-outlined text-[#1a73e8] mt-0.5">check_circle</span>
            <span>Excluded cases are retained for transparency.</span>
          </li>
        </ul>

        <div className="bg-[#fce8e6] text-[#c5221f] p-4 rounded-xl border border-[#fad2cf] mb-4">
          <h4 className="font-bold text-sm mb-1">Limitation</h4>
          <p className="text-sm">Broader prevalence and failure rates are NOT reported because the confirmed sample is too small.</p>
        </div>

        <div className="bg-[#f8f9fa] text-gray-700 p-4 rounded-xl border border-gray-200">
          <h4 className="font-bold text-sm mb-1">Conclusion Limit</h4>
          <p className="text-sm">Part 1 establishes one verified retrieval problem from an audited public-review corpus. The confirmed sample is too small to estimate prevalence, failure rate, or category-level distribution.</p>
        </div>
      </div>
    </section>
  );
}

/* HELPER COMPONENTS */

function PipelineStage({ num, label, onClick, clickable }) {
  return (
    <div 
      onClick={onClick}
      className={`flex-shrink-0 bg-white border border-gray-200 rounded-2xl p-4 min-w-[140px] flex flex-col items-center text-center snap-start shadow-sm transition-shadow ${clickable ? 'cursor-pointer hover:shadow-md' : 'cursor-default'}`}
    >
      <span className="text-2xl font-normal text-[#202124] mb-1">{num}</span>
      <span className="text-[13px] text-gray-500 leading-tight font-medium">{label}</span>
    </div>
  );
}

function PipelineArrow() {
  return (
    <span className="material-symbols-outlined text-gray-300 flex-shrink-0">arrow_forward</span>
  );
}

function CheckItem({ text }) {
  return (
    <li className="flex items-start gap-2.5">
      <span className="material-symbols-outlined text-[#188038] text-[18px] mt-0.5 shrink-0">check_circle</span>
      <span className="text-[14px] text-gray-700 leading-snug">{text}</span>
    </li>
  );
}

function QuestionItem({ text }) {
  return (
    <li className="flex items-start gap-2.5">
      <span className="material-symbols-outlined text-[#d93025] text-[18px] mt-0.5 shrink-0">help</span>
      <span className="text-[14px] text-gray-700 leading-snug">{text}</span>
    </li>
  );
}

function FlowStep({ num, title, desc }) {
  return (
    <div className="flex-1 w-full min-w-[200px] bg-white border border-gray-200 rounded-2xl p-4 flex flex-col items-center text-center shadow-sm hover:shadow-md transition-shadow">
      <span className="w-6 h-6 rounded-full bg-[#f8f9fa] text-gray-600 flex items-center justify-center font-bold text-xs mb-2 border border-gray-200">
        {num}
      </span>
      <span className="text-[14px] font-semibold text-gray-800 mb-1">{title}</span>
      <span className="text-[13px] text-gray-500 leading-snug">{desc}</span>
    </div>
  );
}

function FlowArrow() {
  return (
    <div className="flex items-center justify-center text-gray-300 py-1 md:py-0 shrink-0">
      <span className="material-symbols-outlined hidden md:block">arrow_forward</span>
      <span className="material-symbols-outlined md:hidden">arrow_downward</span>
    </div>
  );
}

function EvidenceMeta({ label, value, isMono }) {
  return (
    <div className="inline-flex items-center gap-1.5 bg-[#f8f9fa] border border-gray-200 px-3 py-1.5 rounded-full shadow-sm hover:shadow-md transition-shadow">
      <span className="text-[11px] text-gray-500 uppercase tracking-wide font-bold">{label}:</span>
      <span className={`text-[13px] text-gray-800 ${isMono ? 'font-mono' : 'font-medium'}`}>{value}</span>
    </div>
  );
}

function AuditItem({ id, desc, color }) {
  const bgColors = {
    blue: 'bg-blue-50 text-[#1967d2] border-blue-100',
    amber: 'bg-[#fef7e0] text-[#b06000] border-[#fce8b2]',
    gray: 'bg-[#f8f9fa] text-gray-700 border-gray-200'
  };
  
  return (
    <div className="flex flex-col gap-1.5 group">
      <span className={`self-start font-mono text-[12px] font-bold px-2 py-0.5 rounded-md border ${bgColors[color]}`}>
        {id}
      </span>
      <p className="text-[14px] text-gray-600 leading-snug pl-1 group-hover:text-gray-900 transition-colors">
        {desc}
      </p>
    </div>
  );
}

function MethodMetric({ num, label }) {
  return (
    <div className="flex flex-col border border-gray-200 rounded-xl px-4 py-2 bg-white shadow-sm hover:shadow-md transition-shadow">
      <span className="text-[18px] font-medium text-gray-800">{num}</span>
      <span className="text-[11px] font-bold text-gray-500 uppercase tracking-wide whitespace-nowrap">{label}</span>
    </div>
  );
}
