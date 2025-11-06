/**
 * Google Apps Script - Simple Test Version for GA4 Statistics
 * 
 * IMPORTANT: 
 * 1. Make sure this code is in a file named "Code.gs" (or rename it)
 * 2. Save the file (Ctrl+S)
 * 3. Deploy as Web App with "New version" selected
 */

// GA4 Property IDs
const PROPERTY_IDS = {
  'vlpim': '12951176208',
  'circular_contact_map': '12951253362',
  'root': '12951280669'
};

// Map tool names to page paths
const PAGE_PATHS = {
  'vlpim': '/VLPIM_Web_services/',
  'circular_contact_map': '/Circular_Contact_Map/',
  'root': '/'
};

/**
 * Main function to handle GET requests
 * This function MUST be named "doGet" for Web App deployment
 */
function doGet(e) {
  const tool = e.parameter.tool || 'all';
  
  try {
    let result;
    
    if (tool === 'all') {
      result = {
        vlpim: getPageViews('vlpim'),
        circular_contact_map: getPageViews('circular_contact_map'),
        root: getPageViews('root'),
        total: 0
      };
      result.total = result.vlpim + result.circular_contact_map + result.root;
    } else {
      const views = getPageViews(tool);
      result = { views: views };
    }
    
    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON)
      .setHeaders({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
      });
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ 
      error: error.toString(),
      message: 'Failed to fetch GA statistics'
    }))
    .setMimeType(ContentService.MimeType.JSON)
    .setHeaders({
      'Access-Control-Allow-Origin': '*'
    });
  }
}

/**
 * Get page views for a specific tool
 * For now, returns 0 as placeholder until Analytics Data API is properly configured
 */
function getPageViews(tool) {
  try {
    const propertyId = PROPERTY_IDS[tool];
    const pagePath = PAGE_PATHS[tool];
    
    if (!propertyId) {
      return 0;
    }
    
    // TODO: Implement Analytics Data API call
    // For now, return 0 as placeholder
    // This allows the doGet function to work and return valid JSON
    
    return 0;
  } catch (error) {
    console.error(`Error fetching page views for ${tool}:`, error);
    return 0;
  }
}

