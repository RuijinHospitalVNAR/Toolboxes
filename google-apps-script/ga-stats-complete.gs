/**
 * Google Apps Script - Complete Implementation for GA4 Statistics
 * 
 * Setup Instructions:
 * 1. Go to https://script.google.com/
 * 2. Create a new project
 * 3. Paste this code
 * 4. Replace PROPERTY_IDS with your GA4 Property IDs
 * 5. Add "Analytics Data API" service (Extensions > Apps Script API)
 * 6. Deploy as Web App (Execute as: Me, Who has access: Anyone)
 * 7. Copy the Web App URL and use it in your HTML files
 */

// GA4 Property IDs (Data Stream IDs)
// VLPIM_Web_services: 12951176208 (G-WT1MXK5JWQ)
// Circular_Contact_Map: 12951253362 (G-H00K0HSQWN)
// Toolboxes (root): 12951280669 (G-F2RPLG89BD)
const PROPERTY_IDS = {
  'vlpim': '12951176208',                // VLPIM_Web_services
  'circular_contact_map': '12951253362', // Circular_Contact_Map
  'af3_helper': '12951280669',           // AF3 Helper (shares root property)
  'root': '12951280669'                  // Toolboxes (root)
};

// Map tool names to page paths in GA4
const PAGE_PATHS = {
  'vlpim': '/VLPIM_Web_services/',
  'circular_contact_map': '/Circular_Contact_Map/',
  'af3_helper': '/AF3_helper/',
  'root': '/'
};

/**
 * Main function to handle GET requests
 */
function doGet(e) {
  // Handle case when e is undefined (e.g., when running from editor)
  if (!e) {
    e = { parameter: {} };
  }
  if (!e.parameter) {
    e.parameter = {};
  }
  
  const tool = e.parameter.tool || 'all';
  const callback = e.parameter.callback; // JSONP callback name
  
  try {
    let result;
    
    if (tool === 'all') {
      // Return aggregated stats for all tools
      result = {
        vlpim: getPageViews('vlpim'),
        circular_contact_map: getPageViews('circular_contact_map'),
        af3_helper: getPageViews('af3_helper'),
        root: getPageViews('root'),
        total: 0
      };
      result.total = result.vlpim + result.circular_contact_map + result.af3_helper + result.root;
    } else {
      // Return stats for specific tool
      const views = getPageViews(tool);
      result = { views: views };
    }
    
    // Ensure result is always a valid object
    if (!result || typeof result !== 'object') {
      result = { error: 'Invalid result', views: 0 };
    }
    
    const jsonData = JSON.stringify(result);
    
    // If callback is provided, return JSONP format; otherwise return JSON
    if (callback) {
      // Validate callback name to prevent XSS (allow alphanumeric, underscore, and $)
      // Remove any characters that are not safe for JavaScript function names
      const safeCallback = callback.replace(/[^a-zA-Z0-9_$]/g, '');
      
      // Only proceed if we have a valid callback name
      if (!safeCallback || safeCallback.length === 0) {
        // Invalid callback name, return safe error
        return ContentService.createTextOutput('console.error("Invalid callback name");')
          .setMimeType(ContentService.MimeType.JAVASCRIPT);
      }
      
      // Return JSONP: callbackName(data)
      // Wrap in try-catch to handle any potential errors
      const jsonpOutput = safeCallback + '(' + jsonData + ');';
      return ContentService.createTextOutput(jsonpOutput)
        .setMimeType(ContentService.MimeType.JAVASCRIPT);
    } else {
      // Return plain JSON
      return ContentService.createTextOutput(jsonData)
        .setMimeType(ContentService.MimeType.JSON);
    }
  } catch (error) {
    // Log error for debugging
    console.error('doGet error:', error);
    
    const errorData = JSON.stringify({ 
      error: error.toString(),
      message: 'Failed to fetch GA statistics'
    });
    
    // If callback is provided, return JSONP format; otherwise return JSON
    if (callback) {
      // Validate callback name
      const safeCallback = callback.replace(/[^a-zA-Z0-9_$]/g, '');
      if (safeCallback && safeCallback.length > 0) {
        return ContentService.createTextOutput(safeCallback + '(' + errorData + ');')
          .setMimeType(ContentService.MimeType.JAVASCRIPT);
      } else {
        // Invalid callback, return error to console
        return ContentService.createTextOutput('console.error("Error: Invalid callback name");')
          .setMimeType(ContentService.MimeType.JAVASCRIPT);
      }
    } else {
      return ContentService.createTextOutput(errorData)
        .setMimeType(ContentService.MimeType.JSON);
    }
  }
}

/**
 * Get page views for a specific tool using GA4 Data API
 */
function getPageViews(tool) {
  try {
    const propertyId = PROPERTY_IDS[tool];
    const pagePath = PAGE_PATHS[tool];
    
    if (!propertyId || propertyId.startsWith('YOUR_')) {
      console.warn(`Property ID not configured for tool: ${tool}`);
      return 0;
    }
    
    // Enable Analytics Data API service in Apps Script first!
    // Extensions > Apps Script API > Add "Analytics Data API"
    
    // Use the Analytics Data API
    const request = {
      property: `properties/${propertyId}`,
      dateRanges: [
        {
          startDate: '2020-01-01', // Start from when you started tracking
          endDate: 'today'
        }
      ],
      dimensions: [
        {
          name: 'pagePath'
        }
      ],
      metrics: [
        {
          name: 'screenPageViews'
        }
      ],
      dimensionFilter: {
        filter: {
          fieldName: 'pagePath',
          stringFilter: {
            matchType: 'EXACT',
            value: pagePath
          }
        }
      }
    };
    
    // Call Analytics Data API
    // Note: You need to enable the Analytics Data API service in Apps Script
    const response = AnalyticsData.Properties.runReport(request, `properties/${propertyId}`);
    
    if (response.rows && response.rows.length > 0) {
      const totalViews = response.rows.reduce((sum, row) => {
        return sum + parseInt(row.metricValues[0].value || 0);
      }, 0);
      return totalViews;
    }
    
    return 0;
  } catch (error) {
    console.error(`Error fetching page views for ${tool}:`, error);
    // Return 0 on error (graceful degradation)
    return 0;
  }
}

/**
 * Alternative: Get total page views (all pages) for a property
 * Useful if you want total views regardless of page path
 */
function getTotalPageViews(propertyId) {
  try {
    const request = {
      property: `properties/${propertyId}`,
      dateRanges: [
        {
          startDate: '2020-01-01',
          endDate: 'today'
        }
      ],
      metrics: [
        {
          name: 'screenPageViews'
        }
      ]
    };
    
    const response = AnalyticsData.Properties.runReport(request, `properties/${propertyId}`);
    
    if (response.rows && response.rows.length > 0) {
      return parseInt(response.rows[0].metricValues[0].value || 0);
    }
    
    return 0;
  } catch (error) {
    console.error('Error fetching total page views:', error);
    return 0;
  }
}

