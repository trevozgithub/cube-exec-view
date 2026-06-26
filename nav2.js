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
  { label: 'Time Reporting',          href: 'timereporting.html', icon: '\u{23F1}️' },
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
  // Prevents tab labels from wrapping on any screen size (27-inch, laptop, tablet, etc.)
  if (!document.getElementById('nav2-styles')) {
    var s = document.createElement('style');
    s.id = 'nav2-styles';
    s.textContent =
      '.topnav-tab { white-space: nowrap !important; }' +
      '.topnav-tabs { min-width: 0; flex-shrink: 1; overflow-x: auto !important; scrollbar-width: none !important; }' +
      '.topnav-tabs::-webkit-scrollbar { display: none !important; }' +
      '@media (max-width: 1700px) {' +
        '.topnav-tab { font-size: 12px !important; padding: 5px 8px !important; gap: 4px !important; }' +
      '}' +
      '@media (max-width: 1400px) {' +
        '.topnav-tab { font-size: 11px !important; padding: 4px 7px !important; gap: 3px !important; }' +
      '}' +
      '@media (max-width: 1150px) {' +
        '.topnav-tab { font-size: 10px !important; padding: 4px 5px !important; gap: 2px !important; }' +
        '.topnav-logo { font-size: 13px !important; }' +
      '}';
    document.head.appendChild(s);
  }
})();
