// CUBE Exec View - Shared Navigation
// Add new pages here; all pages pick up the change automatically.

const PAGES = [
  { label: 'Overview',                href: 'overview.html',      icon: '\u{1F310}' },
  { label: 'Consumer Engineering',    href: 'index.html',         icon: '\u{1F4CA}' },
  { label: 'InfoSec Projects',        href: 'infosec.html',       icon: '\u{1F512}' },
  { label: 'Infrastructure Projects', href: 'infra.html',         icon: '\u{1F3D7}️' },
  { label: 'Content Engineering',     href: 'content.html',       icon: '\u{1F4DD}' },
  { label: 'Corp Tech & WP Systems',  href: 'techops.html',       icon: '\u{1F5A5}️' },
  { label: 'Mid-Market',              href: 'midmarket.html',     icon: '\u{1F4C8}' },
  { label: 'Data & AI',               href: 'dataai.html',        icon: '\u{1F916}' },
  { label: 'Time Reporting',          href: 'timereporting.html', icon: '⏱️' },
  { label: 'Incidents',               href: 'kpi.html',           icon: '\u{1F6A8}' },
];

(function renderNav() {
  var current = location.pathname.split('/').pop() || 'index.html';

  var tabs = PAGES.map(function(p) {
    var active = (current === p.href || (current === '' && p.href === 'index.html')) ? ' active' : '';
    return '<a class="topnav-tab' + active + '" href="' + p.href + '">' + p.icon + ' ' + p.label + '</a>';
  }).join('');

  var addBtn = '<a class="topnav-tab" href="#" onclick="alert(\'Share your next Jira view to add it here!\')">+ Add View</a>';

  document.getElementById('navTabs').innerHTML = tabs + addBtn;

  // Inject responsive nav styles so ALL pages get the fix automatically.
  // Prevents tab labels from wrapping and ensures all tabs are visible on any screen size.
  if (!document.getElementById('nav2-styles')) {
    var s = document.createElement('style');
    s.id = 'nav2-styles';
    s.textContent =
      // Base: 12px so all 11 tabs fit comfortably on 27-inch (2560px) and larger monitors
      '.topnav-tab { white-space: nowrap !important; font-size: 12px !important; padding: 5px 8px !important; gap: 4px !important; }' +
      // Tab strip: fills all available space, scrolls horizontally if needed, no visible scrollbar
      '.topnav-tabs { flex: 1 1 0 !important; min-width: 0; overflow-x: auto !important; scrollbar-width: none !important; }' +
      '.topnav-tabs::-webkit-scrollbar { display: none !important; }' +
      // Hide the date + Open-in-Jira button to give the tab strip full width
      '.topnav-right { display: none !important; }' +
      // Laptop / small external monitor
      '@media (max-width: 1400px) {' +
        '.topnav-tab { font-size: 11px !important; padding: 4px 6px !important; gap: 3px !important; }' +
      '}' +
      // Small screen / tablet landscape
      '@media (max-width: 1150px) {' +
        '.topnav-tab { font-size: 10px !important; padding: 4px 5px !important; gap: 2px !important; }' +
        '.topnav-logo { font-size: 13px !important; }' +
      '}';
    document.head.appendChild(s);
  }
})();
