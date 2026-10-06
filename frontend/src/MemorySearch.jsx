import React, { useState, useRef, useEffect } from 'react';

export default function MemorySearch() {
  const [query, setQuery] = useState("");
  const [memoryContext, setMemoryContext] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [cues, setCues] = useState(null);
  const [candidates, setCandidates] = useState([]);
  
  // Refinement states
  const [activeRejectId, setActiveRejectId] = useState(null);
  const [isRefiningCard, setIsRefiningCard] = useState(null);
  const [cardRefinementQuestion, setCardRefinementQuestion] = useState("");
  const [refineInput, setRefineInput] = useState("");
  
  const [openedPhoto, setOpenedPhoto] = useState(null);
  const [toastMsg, setToastMsg] = useState("");
  const [showToast, setShowToast] = useState(false);

  const displayToast = (msg) => {
    setToastMsg(msg);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000);
  };

  const handleSearch = async () => {
    if (!query) return;
    setIsSearching(true);
    setCues(null);
    setCandidates([]);
    setActiveRejectId(null);

    try {
      const rawApiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const API_BASE = rawApiBase.replace(/\/$/, '');
      
      const payload = { memory: query };
      setMemoryContext(query);

      const res = await fetch(`${API_BASE}/api/retrieval/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) throw new Error("API Request Failed");
      
      const data = await res.json();
      setCues(data.cues);
      setCandidates(data.candidates || []);
      
    } catch (e) {
      displayToast("Error connecting to search backend");
    } finally {
      setIsSearching(false);
    }
  };

  const handleReject = async (photo_id) => {
    setActiveRejectId(photo_id);
    setIsRefiningCard(photo_id);
    setRefineInput("");
    
    try {
      const rawApiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const API_BASE = rawApiBase.replace(/\/$/, '');
      
      const payload = {
          previous_cues: cues,
          additional_memory: "",
          rejected_candidate: photo_id
      };
      
      const res = await fetch(`${API_BASE}/api/retrieval/refine`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) throw new Error("API Request Failed");
      const data = await res.json();
      
      setCardRefinementQuestion(data.refinement_question || "What else do you remember?");
    } catch(e) {
      setCardRefinementQuestion("What else do you remember about this photo?");
    } finally {
      setIsRefiningCard(null);
    }
  };

  const submitRefinement = async (photo_id) => {
    if (!refineInput) return;
    
    setIsSearching(true);
    setActiveRejectId(null);
    
    try {
      const rawApiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const API_BASE = rawApiBase.replace(/\/$/, '');
      
      const payload = {
          previous_cues: cues,
          additional_memory: refineInput,
          rejected_candidate: photo_id
      };
      
      setMemoryContext(prev => prev + ". " + refineInput);
      setRefineInput("");

      const res = await fetch(`${API_BASE}/api/retrieval/refine`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) throw new Error("API Request Failed");
      
      const data = await res.json();
      setCues(data.cues);
      setCandidates(data.candidates || []);
      
    } catch (e) {
      displayToast("Error connecting to search backend");
    } finally {
      setIsSearching(false);
    }
  };

  if (openedPhoto) {
    return (
      <div className="fixed inset-0 z-50 bg-black flex flex-col">
        <header className="p-4 flex justify-between items-center text-white bg-gradient-to-b from-black/50 to-transparent">
          <button onClick={() => setOpenedPhoto(null)} className="p-2 rounded-full hover:bg-white/20">
            <span className="material-symbols-outlined">arrow_back</span>
          </button>
          <div className="flex gap-2">
            <button className="p-2 rounded-full hover:bg-white/20"><span className="material-symbols-outlined">share</span></button>
            <button className="p-2 rounded-full hover:bg-white/20"><span className="material-symbols-outlined">more_vert</span></button>
          </div>
        </header>
        <div className="flex-1 flex items-center justify-center p-4">
          <img src={openedPhoto} alt="Full resolution" className="max-w-full max-h-full object-contain" />
        </div>
      </div>
    );
  }

  return (
    <div className="w-full bg-[#f9f9ff] min-h-[calc(100vh-112px)] flex flex-col font-sans relative pb-24">
      {/* Toast */}
      <div className={`fixed top-32 left-1/2 -translate-x-1/2 z-50 transition-all duration-300 pointer-events-none ${showToast ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-[-8px]'}`}>
        <div className="bg-[#2d3037] text-[#eef0fa] px-4 py-2 rounded-full shadow-lg flex items-center gap-2 text-sm font-medium">
          <span className="material-symbols-outlined text-[#d8e2ff] text-base">info</span>
          <span>{toastMsg}</span>
        </div>
      </div>

      <div className="px-4 md:px-8 mt-6">
        <div className="relative bg-white rounded-full shadow-[0px_2px_8px_rgba(60,64,67,0.12),0px_1px_3px_rgba(60,64,67,0.18)] p-1.5 flex items-center gap-2 max-w-2xl mx-auto">
          <div className="w-10 h-10 rounded-full bg-[#d8e2ff]/50 flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined text-[#005bbf] text-[22px]" style={{fontVariationSettings: "'FILL' 1"}}>auto_awesome</span>
          </div>
          <div className="flex-1 min-w-0 pr-1">
            <p className="text-[11px] text-[#005bbf] tracking-wide uppercase font-semibold flex items-center gap-1 mb-0.5">
              <span>Ask Photos</span>
              {isSearching && <span className="inline-block w-1.5 h-1.5 rounded-full bg-[#005bbf] animate-pulse"></span>}
            </p>
            <input 
              className="w-full bg-transparent border-none outline-none text-sm text-gray-800 placeholder:text-gray-500" 
              placeholder="Describe a photo you vaguely remember..." 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              disabled={isSearching}
            />
          </div>
          <div className="flex items-center gap-1 shrink-0 pr-1">
            <button 
              onClick={() => handleSearch()}
              disabled={!query || isSearching}
              className="w-9 h-9 rounded-full bg-[#1a73e8] hover:bg-blue-700 text-white flex items-center justify-center transition-colors disabled:opacity-50"
            >
              <span className="material-symbols-outlined text-[20px]">search</span>
            </button>
          </div>
        </div>
      </div>

      {isSearching && (
        <div className="flex flex-col items-center justify-center mt-20 text-gray-500 gap-4">
          <div className="w-8 h-8 border-4 border-blue-200 border-t-[#1a73e8] rounded-full animate-spin"></div>
          <p>Searching again...</p>
        </div>
      )}

      {cues && !isSearching && (
        <div className="px-4 md:px-8 mt-8 max-w-3xl mx-auto w-full">
          <div className="bg-[#f1f3fc] rounded-xl p-4 shadow-sm mb-8">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[#005bbf] text-[18px]">psychology</span>
                <h2 className="text-lg font-medium text-[#181c22]">Identified memory cues</h2>
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              {cues.place && cues.place.toUpperCase() !== "UNKNOWN" && (
                <div className="inline-flex items-center gap-1.5 h-8 px-3 rounded-full bg-white text-[#181c22] shadow-sm text-sm">
                  <span className="material-symbols-outlined text-[#005bbf] text-[16px]">location_on</span>
                  <span>{cues.place}</span>
                </div>
              )}
              {cues.people && cues.people.filter(p => p.toUpperCase() !== "UNKNOWN").map(p => (
                <div key={p} className="inline-flex items-center gap-1.5 h-8 px-3 rounded-full bg-white text-[#181c22] shadow-sm text-sm">
                  <span className="material-symbols-outlined text-[#006e2c] text-[16px]">face</span>
                  <span>{p}</span>
                </div>
              ))}
              {cues.event && cues.event.toUpperCase() !== "UNKNOWN" && (
                <div className="inline-flex items-center gap-1.5 h-8 px-3 rounded-full bg-white text-[#181c22] shadow-sm text-sm">
                  <span className="material-symbols-outlined text-[#b81d17] text-[16px]">event</span>
                  <span>{cues.event}</span>
                </div>
              )}
              {cues.approximate_time && cues.approximate_time.toUpperCase() !== "UNKNOWN" && (
                <div className="inline-flex items-center gap-1.5 h-8 px-3 rounded-full bg-white text-[#181c22] shadow-sm text-sm">
                  <span className="material-symbols-outlined text-gray-500 text-[16px]">schedule</span>
                  <span>{cues.approximate_time}</span>
                </div>
              )}
              {cues.visual_details && cues.visual_details.filter(v => v.toUpperCase() !== "UNKNOWN").map(v => (
                <div key={v} className="inline-flex items-center gap-1.5 h-8 px-3 rounded-full bg-[#d8e2ff]/50 text-[#004493] shadow-sm text-sm font-medium">
                  <span className="material-symbols-outlined text-[#005bbf] text-[16px]">visibility</span>
                  <span>{v}</span>
                </div>
              ))}
              {cues.objects && cues.objects.filter(o => o.toUpperCase() !== "UNKNOWN").map(o => (
                <div key={o} className="inline-flex items-center gap-1.5 h-8 px-3 rounded-full bg-[#d8e2ff]/50 text-[#004493] shadow-sm text-sm font-medium">
                  <span className="material-symbols-outlined text-[#005bbf] text-[16px]">category</span>
                  <span>{o}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg text-[#181c22] font-semibold">Possible matches</h3>
            <span className="px-2 py-0.5 rounded-full bg-[#e6e8f1] text-xs text-[#414754]">{candidates.length} found</span>
          </div>

          {candidates.length === 0 ? (
            <div className="bg-white p-8 rounded-xl text-center shadow-sm">
              <span className="material-symbols-outlined text-4xl text-gray-300 mb-2">image_not_supported</span>
              <p className="text-gray-600">No matching photos found in your demo library.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {candidates.map((card) => (
                <article key={card.photo_id} className="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
                  <div className="relative w-full aspect-[4/3] bg-gray-100">
                    <img src={card.image} alt="Candidate" className="w-full h-full object-cover" />
                    <div className="absolute inset-x-0 top-0 p-3 flex items-center justify-between">
                      <div className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-[#005bbf] text-white shadow-sm text-sm font-medium">
                        <span className="material-symbols-outlined text-[16px]" style={{fontVariationSettings: "'FILL' 1"}}>star</span>
                        <span>{card.match_level}</span>
                      </div>
                    </div>
                  </div>
                  <div className="p-4">
                    <div className="flex items-start gap-2 bg-[#d8e2ff]/30 rounded-lg p-3 mb-4">
                      <span className="material-symbols-outlined text-[#005bbf] text-[18px] shrink-0 mt-0.5" style={{fontVariationSettings: "'FILL' 1"}}>auto_awesome</span>
                      <p className="text-sm text-[#181c22]">{card.reason}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <button 
                        onClick={() => setOpenedPhoto(card.image)}
                        className="flex-1 h-11 px-4 rounded-full bg-[#005bbf] text-white text-sm font-medium flex items-center justify-center gap-2 shadow-sm hover:bg-blue-700 transition-colors"
                      >
                        <span className="material-symbols-outlined text-[18px]">photo</span>
                        <span>This is it! Open photo</span>
                      </button>
                      <button 
                        onClick={() => handleReject(card.photo_id)}
                        disabled={activeRejectId === card.photo_id || isRefiningCard === card.photo_id}
                        className="h-11 px-6 rounded-full bg-[#f1f3fc] hover:bg-[#e6e8f1] text-[#414754] text-sm font-medium transition-colors disabled:opacity-50"
                      >
                        Not this one
                      </button>
                    </div>
                  </div>
                  
                  {isRefiningCard === card.photo_id && (
                    <div className="p-6 bg-[#f8f9fe] border-t border-gray-100 flex items-center gap-3 text-gray-500">
                      <div className="w-5 h-5 border-2 border-blue-200 border-t-[#1a73e8] rounded-full animate-spin"></div>
                      <p className="text-sm">Refining your memory...</p>
                    </div>
                  )}

                  {activeRejectId === card.photo_id && !isRefiningCard && (
                    <div className="p-6 bg-[#f8f9fe] border-t border-gray-100">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-[#005bbf] shadow-sm">
                          <span className="material-symbols-outlined text-[18px]">psychology_alt</span>
                        </div>
                        <div>
                          <h4 className="text-[15px] font-medium text-[#181c22]">Let's recover another part of your memory</h4>
                          <p className="text-sm text-[#414754]">{cardRefinementQuestion}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <input 
                          className="flex-1 h-11 px-4 rounded-full bg-white border border-gray-200 text-sm focus:outline-none focus:border-[#005bbf]"
                          placeholder="Add detail..."
                          value={refineInput}
                          onChange={(e) => setRefineInput(e.target.value)}
                          onKeyDown={(e) => e.key === 'Enter' && submitRefinement(card.photo_id)}
                        />
                        <button 
                          onClick={() => submitRefinement(card.photo_id)}
                          disabled={!refineInput}
                          className="h-11 px-6 rounded-full bg-[#1a73e8] text-white text-sm font-medium disabled:opacity-50"
                        >
                          Submit
                        </button>
                      </div>
                    </div>
                  )}
                </article>
              ))}
            </div>
          )}

        </div>
      )}
    </div>
  );
}
