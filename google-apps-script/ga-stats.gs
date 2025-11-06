/**
 * Google Apps Script to fetch Google Analytics 4 statistics
 * 
 * Setup Instructions:
 * 1. Go to https://script.google.com/
 * 2. Create a new project
 * 3. Paste this code
 * 4. Replace PROPERTY_ID with your GA4 Property ID (not Measurement ID)
 * 5. Deploy as Web App (Execute as: Me, Who has access: Anyone)
 * 6. Copy the Web App URL
 */

// Replace with your GA4 Property ID (format: 123456789)
// You can find it in GA4 Admin > Property Settings > Property ID
const PROPERTY_ID = 'YOUR_PROPERTY_ID';

/**
 * Main function to handle GET requests
 */
function doGet(e) {
  const tool = e.parameter.tool || 'all';
  
  try {
    let result;
    
    if (tool === 'all') {
      // Return aggregated stats for all tools
      result = {
        vlpim: getPageViews('vlpim'),
        circular_contact_map: getPageViews('circular_contact_map'),
        root: getPageViews('root'),
        total: 0
      };
      result.total = result.vlpim + result.circular_contact_map + result.root;
    } else {
      // Return stats for specific tool
      const views = getPageViews(tool);
      result = { views: views };
    }
    
    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ 
      error: error.toString() 
    }))
    .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Get page views for a specific tool using GA4 Data API
 */
function getPageViews(tool) {
  try {
    // Map tool names to page paths
    const pagePathMap = {
      'vlpim': '/VLPIM_Web_services/',
      'circular_contact_map': '/Circular_Contact_Map/',
      'root': '/'
    };
    
    const pagePath = pagePathMap[tool] || '/';
    
    // Use Analytics Data API to get page views
    // Note: This requires the Analytics Data API to be enabled
    // and proper authentication setup
    
    // For now, return a placeholder
    // You'll need to implement the actual API call using:
    // https://developers.google.com/analytics/devguides/reporting/data/v1
    
    // Example API call structure:
    /*
    const request = {
      property: `properties/${PROPERTY_ID}`,
      dateRanges: [
        {
          startDate: '2020-01-01',
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
    
    const response = AnalyticsData.Properties.runReport(request, `properties/${PROPERTY_ID}`);
    
    if (response.rows && response.rows.length > 0) {
      return parseInt(response.rows[0].metricValues[0].value) || 0;
    }
    */
    
    return 0; // Placeholder
  } catch (error) {
    console.error('Error fetching page views:', error);
    return 0;
  }
}

